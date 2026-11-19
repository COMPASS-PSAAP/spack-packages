# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Based on the builtin Spack recipe, retargeted at the COMPASS fork and Kokkos 5.

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Parthenon(CMakePackage):
    """A performance portable block-structured adaptive mesh refinement framework."""

    homepage = "https://github.com/parthenon-hpc-lab/parthenon"
    git = "https://github.com/COMPASS-PSAAP/parthenon.git"

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("kokkos-5.3", branch="kokkos-5.3")

    # ------------------------------------------------------------#
    # Variants
    # ------------------------------------------------------------#

    variant("single", default=False, description="Run in single precision")
    variant("mpi", default=True, description="Enable mpi")
    variant(
        "host_comm_buffers", default=False, description="Allocate communication buffers on host"
    )
    variant("hdf5", default=True, description="Enable hdf5")
    with when("+hdf5"):
        variant(
            "compression",
            default=True,
            description="Enable compression in hdf5 output/restart files",
        )
    variant("sparse", default=True, description="Sparse capability")
    variant("ascent", default=False, description="Enable Ascent for in-situ vis and analysis")
    variant("examples", default=False, description="Build example drivers")
    variant("python", default=False, description="Enable python for testing")
    variant(
        "pressure", default=False, description="Registry pressure check for Kokkos CUDA kernels"
    )

    # ------------------------------------------------------------#
    # Dependencies
    # ------------------------------------------------------------#

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.22:", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("hdf5 +mpi", when="+mpi +hdf5")
    depends_on("ascent", when="+ascent")
    depends_on("python@3.5:", when="+python")
    depends_on("kokkos@5.1:")

    conflicts("+host_comm_buffers", when="^kokkos~cuda~rocm")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("PARTHENON_IMPORT_KOKKOS", True),
            self.define_from_variant("PARTHENON_SINGLE_PRECISION", "single"),
            self.define_from_variant("PARTHENON_ENABLE_HOST_COMM_BUFFERS", "host_comm_buffers"),
            self.define_from_variant("CHECK_REGISTRY_PRESSURE", "pressure"),
            self.define_from_variant("PARTHENON_ENABLE_ASCENT", "ascent"),
            self.define("PARTHENON_DISABLE_MPI", not spec.variants["mpi"].value),
            self.define("PARTHENON_DISABLE_HDF5", not spec.variants["hdf5"].value),
            self.define("PARTHENON_DISABLE_HDF5_COMPRESSION", spec.satisfies("~compression")),
            self.define("PARTHENON_DISABLE_SPARSE", not spec.variants["sparse"].value),
            self.define("PARTHENON_DISABLE_EXAMPLES", not spec.variants["examples"].value),
            self.define("BUILD_TESTING", self.run_tests),
        ]
        if spec.satisfies("^kokkos+wrapper"):
            args.append(self.define("CMAKE_CXX_COMPILER", self["kokkos"].kokkos_cxx))
        elif spec.satisfies("^kokkos+rocm") and not (
            spec.satisfies("^kokkos %cxx=clang") or spec.satisfies("^kokkos %cxx=rocmcc")
        ):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
        return args
