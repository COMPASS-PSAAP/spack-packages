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
        help='The name of the cluster to setup files for. For example, "-S $CLUSTER" ',
    )
    parser.add_argument(
        "-E",
        dest="profile_file",
        help="Automatically source Spack setup upon log in by modifying this profile file (e.g., .bashrc).",
    )

    args = parser.parse_args()

    get_update = args.U
    spack_repo_setup = args.R
    profile_file = args.profile_file
    cluster = args.system or os.environ.get("CLUSTER")

    # We only need spack if -R or -E is used
    want_spack = spack_repo_setup or bool(profile_file)

    # 2. Check for CLUSTER availability
    if not cluster:
        print(f"{red}No system specified -- exiting.{black}")
        sys.exit(1)

    cwd = Path.cwd()
    cluster_dir = cwd / "system_externals" / cluster

    # 3. Check if we know about the cluster
    if not cluster_dir.is_dir():
        print(f"{red}No packages for system -- exiting.{black}")
        sys.exit(1)

    # 4. Setup install directories
    install_file = cluster_dir / "packages.yaml"
    home = Path.home()
    install_location = home / ".spack" / cluster

    if not install_location.is_dir():
        print(f"{green}Making folder for {cluster} external/system packages{black}")
        install_location.mkdir(parents=True, exist_ok=True)

    # 5. Check if file is present and needs updating
    target_file = install_location / "packages.yaml"
    need_new_file = False

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

    # Install the package file if needed
    if need_new_file:
        print(f"{green}Installing {install_file} to {install_location}{black}")
        shutil.copy2(install_file, install_location)

    # 6. Update git repository
    if get_update:
        print(f"{blue}Pulling latest code:{black}")
        subprocess.run(["git", "pull"], check=True)

    # 7. Stop here if Spack-specific actions are not requested
    if not want_spack:
        sys.exit(0)

    # 8. Check for Spack installation
    spack_exe = shutil.which("spack")
    if not spack_exe:
        print("No spack installed -- stopping")
        sys.exit(1)

    # 8b Get true path
    full_path = spack_exe.replace("bin/spack", "share/spack/setup-env.sh")

    # 9. Setup Spack repositories
    if spack_repo_setup:
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

        strings_to_add = [
            "export SPACK_USER_CONFIG_PATH=$HOME/.spack/$CLUSTER",
            f"source {full_path}",
        ]

        for string_to_add in strings_to_add:
            # Read existing content to check if string is already present
            with open(profile_path, "r") as f:
                lines = [line.strip() for line in f.readlines()]

            if string_to_add not in lines:
                print(f'{green}Adding "{string_to_add}" to "{profile_path}".{black}')
                with open(profile_path, "a") as f:
                    f.write(f"\n{string_to_add}\n")
            else:
                print(
                    f'{blue}{string_to_add}" already present in requested file. Skipping.{black}'
                )


if __name__ == "__main__":
    main()
