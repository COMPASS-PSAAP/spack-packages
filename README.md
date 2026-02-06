## About:
This repository contains a Spack package repository with custom Spack package files for various applications and libraries made and utilized by COMPASS.

This repository is a fork of the CUP-ECS PSAAP-III repo by the same name. The package files from this project are still included as a separate Spack repository.

## Setup:
  1. Clone Spack from https://github.com/spack/spack.
  2. Clone this repository.
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
