#!/usr/bin/env python3

import argparse
import os
import sys
import shutil
import hashlib
import subprocess
from pathlib import Path

# Global variables for colors:
black = "\033[0m"
red = "\033[91m"
green = "\033[92m"
blue = "\033[94m"


def get_sha1(filepath):
    """Calculate the SHA1 hash of a file."""
    h = hashlib.sha1()
    h.update(filepath.read_bytes())
    return h.hexdigest()


def main():
    # 1. Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Setup Spack custom repositories and configuration.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Notes:
  -R: It is a good idea to check in all code in "spack develop" before running this command!
  -S: This is destructive and will override any local adjustments to your system packages and/or repo package.yaml files!
  -E: This command is currently setup to add a LLNL specific command to the provided file. If not on an LLNL machine, please
      remove this line (or set the appropriate variable to the file).
      This command also wants the path to the file from $HOME, not the current directory.
  -C with -E: Will not write "export SPACK_USER_CONFIG_PATH=< >" to the specified file.
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
        "-C",
        action="store_true",
        help="Use SPACK_USER_CONFIG_PATH environment variable for install location of the system packages file.",
    )
    parser.add_argument(
        "-S",
        dest="system",
        help='The name of the cluster to setup files for. For example, "-S $CLUSTER" ',
    )
    parser.add_argument(
        "-E",
        dest="profile_file",
        help="Automatically source Spack setup upon log in by modifying this profile file (e.g., .bashrc).",
    )

    args = parser.parse_args()

    profile_file = args.profile_file
    cluster = args.system or os.environ.get("CLUSTER")

    # 2. Update git repository
    if args.U:
        print(f"{blue}Pulling latest code:{black}")
        subprocess.run(["git", "pull"], check=True)

    # 3. Check for CLUSTER availability
    if not cluster:
        print(f"{red}No system specified -- exiting.{black}")
        sys.exit(1)

    cwd = Path.cwd()
    cluster_dir = cwd / "system_externals" / cluster

    # 4. Check if we know about the cluster
    if not cluster_dir.is_dir():
        print(f"{red}No packages for system -- exiting.{black}")
        sys.exit(1)

    # 5. Setup install directories
    install_file = cluster_dir / "packages.yaml"
    home = Path.home()
    # 5a. Determine location to install to
    if args.C:
        env_config_path = os.environ.get("SPACK_USER_CONFIG_PATH")
        if not env_config_path:
            print(
                f"{red}-C flag provided, but SPACK_USER_CONFIG_PATH is not set in the environment -- exiting.{black}"
            )
            sys.exit(1)
        install_location = Path(env_config_path)
    else:
        install_location = home / ".spack" / cluster

    if not install_location.is_dir():
        print(
            f"{green}Making folder for {cluster} external/system packages at {install_location}{black}"
        )
        install_location.mkdir(parents=True, exist_ok=True)

    # 6. Install system-specific packages.yaml
    target_file = install_location / "packages.yaml"
    need_new_file = False

    # 6a. Check if file is present and needs updating
    if target_file.is_file():
        hash1 = get_sha1(install_file)
        hash2 = get_sha1(target_file)
        if hash1 != hash2:
            print(
                f"{blue}Current packages file ({target_file}) does not match repo, will replace{black}"
            )
            need_new_file = True
    else:
        need_new_file = True

    # 6b. Install the package file, if needed
    if need_new_file:
        print(f"{green}Installing {install_file} to {install_location}{black}")
        shutil.copy2(install_file, install_location)
    else:
        print(f'{blue}No new "package.yaml" file installed.{black}')

    # 7. Stop here if Spack-specific actions are not requested
    if not (args.R or bool(profile_file)):
        sys.exit(0)

    # 8. Check for Spack installation
    spack_exe = shutil.which("spack")
    if not spack_exe:
        print(f"{red}No spack installed -- stopping{black}")
        sys.exit(1)

    # 8b Get true path
    full_path = spack_exe.replace("bin/spack", "share/spack/setup-env.sh")

    # 9. Setup Spack repositories
    if args.R:
        print(f"{green}Reestablishing Spack repositories:{black}")
        repos_to_process = ["cupecs", "compass"]

        for repo in repos_to_process:
            # Suppress errors on removal in case they don't exist yet
            subprocess.run(
                [spack_exe, "repo", "remove", f"{repo}"], stderr=subprocess.DEVNULL
            )
            subprocess.run(
                [
                    spack_exe,
                    "repo",
                    "add",
                    str(cwd / "spack_pkgs" / "spack_repo" / f"{repo}"),
                ],
                check=True,
            )

    # 10. Modify user profile
    if profile_file:
        profile_path = home / profile_file
        if not profile_path.is_file():
            print(f"{red}{profile_path} does not exist -- stopping{black}")
            sys.exit(1)

        # Structure strings to add alongside any flags that should cause them to be skipped
        strings_to_process = [
            {
                "text": "export SPACK_USER_CONFIG_PATH=$HOME/.spack/$CLUSTER",
                "conflicts_with": [args.C],  # Skips if -C is True
            },
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


if __name__ == "__main__":
    main()
