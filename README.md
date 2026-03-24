## About:
This repository contains a Spack package repository with custom Spack package files for various applications and libraries made and utilized by COMPASS.

This repository is a fork of the CUP-ECS PSAAP-III repo by the same name. The package files from this project are still included as a separate Spack repository.

## Automatic Setup:
This project provides a helper script (`spack_setup_script.py`) that can take care of setting up system-specific package files as well as tweaking a few Spack settings for you. For the first run of the script, you will generally do something like the following (which is specific to an LLNL machine):
```bash
# Basic Usage
python3 spack_setup_script.py -R -S $CLUSTER
# Advanced Usage -- The file after "-E" depends on your setup
python3 spack_setup_script.py -U -R -S $CLUSTER -E .bashrc
```
Some options require Spack to be loaded in the environment, so it is a good idea to make sure that it is loaded before you run this tool. We've set this script up with output messages that outline what it is doing, but the individual steps are also outlined in the python file itself. To update your local files with any potential updates, add the `-U` flag to have the script do a `git pull` before running. For more details on the flags, run with `--help`

## Manual Setup:
  1. Set up your environment so that Spack is loaded.
  2. Point Spack to the git repo with this command:
```bash
  # Note: "COMPASSRepo" will be the name to give to spack when doing "spack repo update" or "spack repo remove"
  # The path at the end of this command may also be changed, if so desired.
  spack repo add --name COMPASSRepo https://github.com/COMPASS-PSAAP/spack-packages.git ~/.spack/package_repos/COMPASS
```
  3. Run `spack repo list` to verify Spack has found the package _namespaces_ correctly. The output should be similar to:
```
[+] cupecs     v2.0    /g/g16/derek/.spack/package_repos/COMPASS/spack_pkgs/spack_repo/cupecs
[+] compass    v1.0    /g/g16/derek/.spack/package_repos/COMPASS/spack_pkgs/spack_repo/compass
[+] builtin    v2.2    /g/g16/derek/.spack/package_repos/fncqgg4/repos/spack_repo/builtin
```
 4. Run `spack config get repos` to verify Spack has setup the external package _repository_ correctly. The output should be similar to:
```yaml
repos:
  COMPASSRepo:
    git: https://github.com/COMPASS-PSAAP/spack-packages.git
    destination: /g/g16/derek/.spack/package_repos/COMPASS
  builtin:
    git: https://github.com/spack/spack-packages.git
    branch: releases/v2025.11
```
 5. Use Spack normally. Spack will automatically find libraries included in this repository.
 6. If Spack files for described packages already installed on the system are wanted, clone this repository and copy the system package file from `system_externals` to the location your Spack install is set up to look at (i.e., the value of `SPACK_USER_CONFIG_PATH`.) Be sure to reload/relog if doing this while Spack is active.


## Package Creation:
Create a directory with the name of your package in `spack_pkgs/spack_repo/compass/packages` and place your `package.py` file in that directory.

For packages that include `CMakePackage`, `CudaPackage`, and/or `ROCmPackage`, you must include the following imports in your `packages.py` file:
```python
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
```
And for other spack-related functions, import:
```python
from spack.package import *
```

## System External Packages
This repository is also home to the collection of Spack `package.yaml` files that describe to Spack the external packages already on the system. These files can be found in the `system_externals` folder, and each file has a version number for easy comparison between versions. Currently, the following systems are available:
- Dane
- Tuolumne