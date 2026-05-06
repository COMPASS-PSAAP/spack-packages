# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *

class Canopy(CMakePackage, CudaPackage, ROCmPackage):
    """Locality-aware optimizations for standard MPI collectives as well as neighborhood collectives."""

    homepage = "https://github.com/JStewart28/Canopy"
    git = "https://github.com/JStewart28/Canopy.git"

    maintainers("JStewart28")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=True)
    version("master", branch="master", submodules=True)
    
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    
    # Google test
    depends_on("googletest", type="build")

    # Variants are primarily backends to build on GPU systems and pass the right
    # informtion to the packages we depend on
    variant("cuda", default=False, description="Use CUDA support from subpackages")
    variant("openmp", default=False, description="Use OpenMP support from subpackages")
    variant("rocm", default=False, description="Use ROCM support from subpackages")
    variant("testing", default=False, description="Build and install tests")
    variant("examples", default=False, description="Build and install examples")
    
    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+rocm", when="amdgpu_target=none")
        
    # Cabana general depdendencies
    depends_on("cabana @master +grid +mpi +arborx", when="@develop")
    depends_on("cabana @master +grid +mpi +arborx", when="@master")

    # Cabana GPU depdendencies
    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on(f"cabana {cuda_dep}", when=cuda_dep)

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on(f"cabana {rocm_dep}", when=rocm_dep)

    # If we're using CUDA or ROCM, require MPIs be GPU-aware
    conflicts("mpich ~cuda", when="+cuda")
    conflicts("mpich ~rocm", when="+rocm")
    conflicts("openmpi ~cuda", when="+cuda")
    conflicts("^intel-mpi")  # Heffte won't build with intel MPI because of needed C++ MPI support
    # Commenting so we can test C++20 and cuda@12.2.1 on Lassen
    # conflicts("^spectrum-mpi", when="^cuda@11.3:") # cuda-aware spectrum is broken with cuda 11.3:


    # CMake specific build functions
    def cmake_args(self):
        options = []

        enable = ["EXAMPLES", "TESTING"]
        require = []

        for category, cname in zip([enable, require], ["ENABLE", "REQUIRE"]):
            for var in category:
                canopy_option = f"Canopy_{cname}_{var}"
                options.append(self.define_from_variant(canopy_option, var.lower()))

        # If testing is enabled, also install the tests
        options.append(self.define_from_variant("Canopy_INSTALL_TEST_EXECUTABLES", "testing"))

        # If examples are enabled, also install the examples
        options.append(self.define_from_variant("Canopy_INSTALL_EXAMPLES", "examples"))

        # Use hipcc as the c compiler if we are compiling for rocm. Doing it this way
        # keeps the wrapper insted of changeing CMAKE_CXX_COMPILER keeps the spack wrapper
        # and the rpaths it sets for us from the underlying spec.
        # if self.spec.satisfies("+rocm"):
            # options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))

        # If we're building with cray mpich, we need to make sure we get the GTL library for
        # gpu-aware MPI
        # if self.spec.satisfies("+rocm ^cray-mpich"):
            # gtl_dir = join_path(self.spec["cray-mpich"].prefix, "..", "..", "..", "gtl", "lib")
            # options.append(
                # "-DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath={0} -L{0} -lmpi_gtl_hsa".format(gtl_dir)
            # )
        # elif self.spec.satisfies("+cuda ^cray-mpich"):
            # gtl_dir = join_path(self.spec["cray-mpich"].prefix, "..", "..", "..", "gtl", "lib")
            # options.append(
                # "-DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath={0} -L{0} -lmpi_gtl_cuda".format(gtl_dir)
            # )
        return options
