# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage
from spack_repo.builtin.packages.kokkos.package import Kokkos

from spack.package import *

class Cabanafluids(CMakePackage, CudaPackage, ROCmPackage):
    """Fluid advection benchmark for exploring stream-triggered halo exchanges and sparse matrix methods in the Cabana/Cajita performance portability framework."""

    homepage = "https://github.com/CUP-ECS/CabanaFluids"
    git = "https://github.com/CUP-ECS/CabanaFluids.git"

    maintainers("patrickb314")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("main", branch="main")
    version("0.9.0", tag="v0.9.0", commit="743cd4085546e2be920c1eee19ca8c4afd3dead7")

    # Variants are primarily backends to build on GPU systems and pass the right
    # informtion to the packages we depend on
    variant("cuda", default=False, description="Use CUDA support from subpackages")
    variant("rocm", default=False, description="Use ROCM support from subpackages")
    variant("openmp", default=False, description="Use OpenMP support from subpackages")
    variant("hypre", default=False, description="Include support for hypre structured solver in addition to the included reference solver.")

    # Dependencies for all CabanaFluids versions
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("mpi", type="build")

    # Kokkos dependencies
    depends_on("kokkos @4:")

    # Cabana dependencies
    depends_on("cabana @0.7.0: +grid +silo +mpi") # Base cabana features we need
    depends_on("cabana +hypre", when="+hypre") # If we want hypre

    # Make sure we have the serial backend if we don't have cuda or rocm
    depends_on("cabana +serial", when="~cuda~rocm")
    depends_on("cabana +serial", when="~hypre") # serial is reliable if we don't have hypre, too

    # Silo dependencies
    depends_on("silo @4.11:")
    depends_on("silo @4.11.1:", when="%cce")  # Eariler silo versions have trouble cce

    # Google test for test cases
    depends_on("googletest", type="build")

    # If we're using CUDA or ROCM, require MPIs be GPU-aware
    conflicts("mpich ~cuda", when="+cuda")
    conflicts("mpich ~rocm", when="+rocm")
    conflicts("openmpi ~cuda", when="+cuda")
    conflicts("^spectrum-mpi", when="^cuda@11.3:")  # cuda-aware spectrum is broken with cuda 11.3:

    # CMake specific build functions
    def cmake_args(self):
        args = []

        # Use hipcc as the c compiler if we are compiling for rocm. Doing it this way
        # keeps the wrapper insted of changing CMAKE_CXX_COMPILER keeps the spack wrapper
        # and the rpaths it sets for us from the underlying spec.
        if "+rocm" in self.spec:
            env["SPACK_CXX"] = self.spec["hip"].hipcc

        # If we're building with cray mpich, we need to make sure we get the GTL library for
        # gpu-aware MPI, since cabana requires it
        if self.spec.satisfies("+rocm ^cray-mpich"):
            gtl_dir = join_path(self.spec["cray-mpich"].prefix, "..", "..", "..", "gtl", "lib")
            args.append(
                "-DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath={0} -L{0} -lmpi_gtl_hsa".format(gtl_dir)
            )
        elif self.spec.satisfies("+cuda ^cray-mpich"):
            gtl_dir = join_path(self.spec["cray-mpich"].prefix, "..", "..", "..", "gtl", "lib")
            args.append(
                "-DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath={0} -L{0} -lmpi_gtl_cuda".format(gtl_dir)
            )
        return args
