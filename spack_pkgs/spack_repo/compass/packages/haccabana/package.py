# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Haccabana(CMakePackage):
    """HACCabana: A proxy app for HACC short range forces.
    The Hardware/Hybrid Accelerated Cosmology Code (HACC), a cosmology
    N-body-code framework, is designed to run efficiently on diverse computing
    architectures and to scale to millions of cores and beyond."""

    homepage = "https://github.com/COMPASS-PSAAP/HACCabana.git"
    git = "https://github.com/COMPASS-PSAAP/HACCabana.git"

    maintainers("steverangel", "adrianpope", "streeve", "junghans", "JStewart28")

    tags = ["proxy-app", "ecp-proxy-app"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("develop", branch="develop")

    variant("shared", default=True, description="Build shared libraries")
    variant("cuda", default=False, description="Use CUDA support from subpackages")
    variant("openmp", default=False, description="Use OpenMP support from subpackages")
    variant("rocm", default=False, description="Use ROCM support from subpackages")

    variant("canopy", default=False, description="Fast multipole solver for far field forces")

    depends_on("cxx", type="build")

    depends_on("cmake@3.9:", type="build")
    depends_on("kokkos@3.0:")
    depends_on("cabana@master")

    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+rocm", when="amdgpu_target=none")

    # Cabana GPU depdendencies
    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on(f"cabana {cuda_dep}", when=cuda_dep)
        depends_on(f"canopy {cuda_dep}", when=f"+canopy {cuda_dep}")

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on(f"cabana {rocm_dep}", when=rocm_dep)
        depends_on(f"canopy {rocm_dep}", when=f"+canopy {rocm_dep}")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        enable = []
        require = ["CANOPY"]

        for category, cname in zip([enable, require], ["ENABLE", "REQUIRE"]):
            for var in category:
                haccabana_option = f"HACCabana_{cname}_{var}"
                options.append(self.define_from_variant(haccabana_option, var.lower()))

        return options