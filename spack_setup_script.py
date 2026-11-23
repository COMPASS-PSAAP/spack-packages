#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import subprocess
from pathlib import Path

# Global variables for colors:
black = "\033[0m"
red = "\033[91m"
green = "\033[92m"
blue = "\033[94m"


def main():
    # 1. Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Setup Spack custom repositories and configuration.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Notes:
  -R: It is a good idea to check in all code in "spack develop" before running this command!
  -R: Also includes system_externals/include.yaml from your Spack user scope, which applies each
      supported system's configuration on that system only. Set COMPASS_SYSTEM to choose a system by hand.
  -E: This command wants the path to the file from $HOME, not the current directory.
  -R, -E: These options require Spack to be available in the environment.
""",
    )
    parser.add_argument(
        "-U", action="store_true", help='Do a "git pull" before installing.'
    )
    parser.add_argument(
        "-R",
        action="store_true",
        help="Install custom CUP-ECS and COMPASS Spack package repositories.",
    )
    parser.add_argument(
        "-S",
        dest="system",
        help="No longer needed: Spack now detects the system. Set COMPASS_SYSTEM to choose one by hand.",
    )
    parser.add_argument(
        "-E",
        dest="profile_file",
        help="Automatically source Spack setup upon log in by modifying this profile file (e.g., .bashrc).",
    )

    args = parser.parse_args()

    profile_file = args.profile_file
    home = Path.home()

    if args.system:
        print(
            f"{blue}-S is no longer needed: Spack detects the system. Set COMPASS_SYSTEM to choose one by hand.{black}"
        )

    # 2. Update git repository
    if args.U:
        print(f"{blue}Pulling latest code:{black}")
        subprocess.run(["git", "pull"], check=True)

    # 3. Stop here if Spack-specific actions are not requested
    if not (args.R or bool(profile_file)):
        sys.exit(0)

    # 4. Check for Spack installation
    spack_exe = shutil.which("spack")
    if not spack_exe:
        print(f"{red}No spack installed -- stopping{black}")
        sys.exit(1)

    # 4b Get true path
    full_path = spack_exe.replace("bin/spack", "share/spack/setup-env.sh")

    # 5. Setup Spack repositories
    if args.U and args.R:
        print(f"{green}Updating external COMPASS Spack repositories:{black}")
        subprocess.run(
            [spack_exe, "repo", "update", "COMPASSRepo"], stderr=subprocess.DEVNULL
        )
    elif args.R:
        print(f"{green}Establishing external COMPASS Spack repositories:{black}")
        subprocess.run(
            [
                spack_exe,
                "repo",
                "add",
                "--name",
                "COMPASSRepo",
                "https://github.com/COMPASS-PSAAP/spack-packages.git",
                "~/.spack/package_repos/COMPASS",
            ],
            stderr=subprocess.DEVNULL,
        )

    # 6. Include the system configuration from the user scope
    if args.R:
        install_system_include(home)

    # 7. Modify user profile
    if profile_file:
        profile_path = home / profile_file
        if not profile_path.is_file():
            print(f"{red}{profile_path} does not exist -- stopping{black}")
            sys.exit(1)

        # Structure strings to add alongside any flags that should cause them to be skipped
        strings_to_process = [
            {
                "text": f"source {full_path}",
                "conflicts_with": [],  # Always writes if -E is used
            },
        ]

        for item in strings_to_process:
            # If any conflicting flag in the list is True, skip this string
            if any(item["conflicts_with"]):
                print(
                    f"{blue}Skipping '{item['text']}' due to conflicting flag.{black}"
                )
                continue

            string_to_add = item["text"]

            # Read existing content to check if string is already present
            with open(profile_path, "r") as f:
                lines = [line.strip() for line in f.readlines()]

            if string_to_add not in lines:
                print(f'{green}Adding "{string_to_add}" to "{profile_path}".{black}')
                with open(profile_path, "a") as f:
                    f.write(f"\n{string_to_add}\n")
            else:
                print(
                    f'{blue}"{string_to_add}" already present in requested file. Skipping.{black}'
                )


def install_system_include(home):
    """Include system_externals/include.yaml, from the copy of this repository
    that Spack keeps up to date, in the Spack user scope."""
    include_path = "~/.spack/package_repos/COMPASS/system_externals/include.yaml"
    # Spack fails on every command when a required include is missing, as it
    # is in a copy cloned before this file existed
    if not Path(include_path).expanduser().is_file():
        print(
            f"{red}{include_path} does not exist; update the repository with -U -R, then rerun -R.{black}"
        )
        sys.exit(1)
    config_path = os.environ.get("SPACK_USER_CONFIG_PATH")
    user_scope = Path(config_path) if config_path else home / ".spack"

    # Earlier versions of this script copied a system's packages.yaml into
    # ~/.spack/$CLUSTER and pointed SPACK_USER_CONFIG_PATH there. That copy
    # sits above the include and would override it with stale settings.
    if config_path:
        print(
            f"{red}SPACK_USER_CONFIG_PATH is set to {config_path}. Earlier versions of this script set it to "
            f"$HOME/.spack/$CLUSTER; if so, remove that line from your profile, log in again, and rerun -R.{black}"
        )
        if (user_scope / "packages.yaml").is_file():
            print(
                f"{red}{user_scope / 'packages.yaml'} may be a copy of a system's packages.yaml from an "
                f"earlier version of this script; it would override the included one.{black}"
            )

    include_file = user_scope / "include.yaml"
    if not include_file.is_file():
        user_scope.mkdir(parents=True, exist_ok=True)
        print(f"{green}Including the COMPASS system configuration from {include_file}{black}")
        include_file.write_text(f"include:\n- path: {include_path}\n")
    elif include_path in include_file.read_text():
        print(f"{blue}{include_file} already includes the COMPASS system configuration.{black}")
    else:
        print(
            f"{red}{include_file} exists; add this entry to its include list by hand:{black}\n"
            f"- path: {include_path}"
        )


if __name__ == "__main__":
    main()
