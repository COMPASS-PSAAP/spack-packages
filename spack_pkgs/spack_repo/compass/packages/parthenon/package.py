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

    @property
    def uses_cray_gtl(self):
        """Cray MPICH needs its GPU transport layer to send device buffers."""
        spec = self.spec
        return spec.satisfies("+mpi ~host_comm_buffers ^[virtuals=mpi] cray-mpich") and (
            spec.satisfies("^kokkos+rocm") or spec.satisfies("^kokkos+cuda")
        )

    def flag_handler(self, name, flags):
        # CMake's MPI detection does not know about the GTL, so pass its
        # link flags through CMake
        build_system_flags = []
        if self.uses_cray_gtl:
            build_system_flags = self.spec["cray-mpich"].package.gtl_lib.get(name, [])
        return (flags, None, build_system_flags)

    def setup_build_environment(self, env):
        # Have Spack's compiler wrapper call hipcc or nvcc_wrapper, rather
        # than replacing the wrapper, so it still adds the spec's rpaths
        spec = self.spec
        if spec.satisfies("^kokkos+wrapper"):
            env.set("SPACK_CXX", self["kokkos"].kokkos_cxx)
        elif spec.satisfies("^kokkos+rocm") and not (
            spec.satisfies("^kokkos %cxx=clang") or spec.satisfies("^kokkos %cxx=rocmcc")
        ):
            env.set("SPACK_CXX", spec["hip"].hipcc)
        self.setup_run_environment(env)

    def setup_run_environment(self, env):
        if self.uses_cray_gtl:
            env.set("MPICH_GPU_SUPPORT_ENABLED", "1")
        if self.spec.satisfies("^kokkos+apu"):
            env.set("HSA_XNACK", "1")

    def cmake_args(self):
        spec = self.spec
        return [
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
