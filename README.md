## About:
This repository contains a Spack package repository with custom Spack package files for various applications and libraries made and utilized by COMPASS.

This repository is a fork of the CUP-ECS PSAAP-III repo by the same name. The package files from this project are still included as a separate Spack repository.

## Requirements:
These packages require Spack 1.2 or newer, which uses the builtin package repository from `releases/v2026.06`. Older builtin releases lack Kokkos 5, which Parthenon needs, and use a Kokkos recipe format that the `cupecs` Cabana package cannot load. To get a suitable Spack:
```bash
git clone --depth=2 --branch=releases/v1.2 https://github.com/spack/spack.git ~/spack
. ~/spack/share/spack/setup-env.sh
```

## Automatic Setup:
This project provides a helper script (`spack_setup_script.py`) that can take care of setting up system-specific package files as well as tweaking a few Spack settings for you. For the first run of the script, you will generally do something like the following, on any system:
```bash
# Basic First-time Setup
python3 spack_setup_script.py -R
# Advanced First-time Setup -- The file after "-E" depends on your setup
python3 spack_setup_script.py -R -E .bashrc
# Getting Updates (-E is not needed, but can be added if not used before)
python3 spack_setup_script.py -U -R
```
Some options require Spack to be loaded in the environment, so it is a good idea to make sure that it is loaded before you run this tool. We've set this script up with output messages that outline what it is doing, but the individual steps are also outlined in the python file itself. To update your local files with any potential updates, add the `-U` flag to have the script do a `git pull` before running. In addition to updating this Git repository, running with `-U` with `-R` will also request Spack to pull the updates for the Spack package repositories provided by this project, though Spack will do nothing if `-R` has not been previously run without `-U`. For more details on the flags, run with `--help`

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
    branch: releases/v2026.06
```
 5. Use Spack normally. Spack will automatically find libraries included in this repository.
 6. To use the configuration for the systems in `system_externals`, include it from your Spack user scope by adding this to `~/.spack/include.yaml` (the path is the destination from step 2):
```yaml
include:
- path: ~/.spack/package_repos/COMPASS/system_externals/include.yaml
```


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
This repository is also home to the collection of Spack configuration for each system: `packages.yaml` files that describe to Spack the external packages already on the system, and any other settings a system needs, such as Easley's `upstreams.yaml`. These files can be found in the `system_externals/<system>` folders, and each file has a version number for easy comparison between versions.

`system_externals/include.yaml` includes each system's folder on that system only, and `-R`, or step 6 of the manual setup, includes it from your user scope. Spack evaluates its conditions every time it starts, so a home directory shared by several clusters gets the right configuration on each, and `spack repo update COMPASSRepo` (or `-U -R`) updates it along with the packages. Each system is recognized from, in order:
- `COMPASS_SYSTEM`, which you can set to a folder name to choose a system by hand
- otherwise, a pattern on the system's hostnames

Run `spack config scopes -p` to see which system Spack chose; its folder appears as a `compass-<system>` scope. To add a system, add its folder and an entry in `system_externals/include.yaml`.

Earlier versions of the setup script copied a system's `packages.yaml` into `~/.spack/$CLUSTER` and added `export SPACK_USER_CONFIG_PATH=$HOME/.spack/$CLUSTER` to your profile. That variable moves your user scope, so Spack would not read `~/.spack/include.yaml`, and the copied file would override the included one. Remove the line from your profile, log in again, and rerun the script with `-R`; any settings of your own in `~/.spack/$CLUSTER` move to `~/.spack`.

Currently, the following systems are available:
- Dane
- Tuolumne
- Easley (UNM CARC), which upstreams to CARC's Spack installation
- Hopper (UNM CARC), which upstreams to CARC's Spack installation

## Testing on HPC Systems

Agents may not run on LLNL systems or on Easley, so a check of a change
there goes through `working/`, the exchange from
`COMPASS-PSAAP/compass-template`: an agent writes a request on a feature
branch, and a person runs it with `working/bin/run-request`, which commits
the results to the branch. `working/README.md` describes the protocol.
Requests never reach `main`; remove them and squash-merge, as that file
says.
