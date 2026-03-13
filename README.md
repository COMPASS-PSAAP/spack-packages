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
  1. Clone this repository.
  2. Clone Spack from https://github.com/spack/spack.
  3. Set up your environment so that Spack is loaded.
  4. Add the repositories to Spack by running:
```bash
spack repo add /path/to/this/repo/spack_pkgs/spack_repo/cupecs
spack repo add /path/to/this/repo/spack_pkgs/spack_repo/compass
```
  5. Run `spack repo list` to verify Spack has found the package repositories correctly. The output should be similar to:
```
[+] compass    v1.0    /home/theta/git/spack-packages/spack_pkgs/spack_repo/compass
[+] cupecs     v2.0    /home/theta/git/spack-packages/spack_pkgs/spack_repo/cupecs
[+] builtin    v2.2    /home/theta/.spack/package_repos/fncqgg4/repos/spack_repo/builtin
```
 6. Use Spack normally. Spack will automatically find libraries included in this repository.
 7. Copy the system package file from `system_externals` to the location your Spack install is set up to look at (i.e., the value of `SPACK_USER_CONFIG_PATH`.)


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