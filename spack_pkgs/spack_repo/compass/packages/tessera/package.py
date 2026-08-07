# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *

class Tessera(CMakePackage, CudaPackage, ROCmPackage):
    """Distributed, MPI- and GPU-aware unstructured triangle-mesh library
    built on Cabana and Kokkos."""

    homepage = "https://github.com/JStewart28/Tessera"
    git = "https://github.com/JStewart28/Tessera.git"

    maintainers("JStewart28")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=True)
    version("master", branch="master", submodules=True)

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Variants are primarily backends to build on GPU systems and pass the right
    # information to the packages we depend on
    variant("cuda", default=False, description="Require CUDA support from Kokkos")
    variant("openmp", default=False, description="Require OPENMP support from Kokkos")
    variant("rocm", default=False, description="Require ROCM support from Kokkos")
    variant("threads", default=False, description="Require THREADS support from Kokkos")
    variant("testing", default=False, description="Build and install tests")
    variant("examples", default=False, description="Build and install examples")
    variant("profiling", default=False, description="Enable Tessera internal profiling")
    variant(
        "debug",
        default=True,
        description=(
            "Enable Tessera runtime debug checks (e.g. the stale-handle "
            "generation guard on Mesh slice/CSR/key-View accessors)"
        ),
    )
    variant(
        "profiling_level",
        default="default",
        values=("default", "0", "1", "2", "3"),
        multi=False,
        description=(
            "Profiling detail level: 0=off, 1=basic phases, 2=detailed "
            "sub-phases, 3=verbose (reserved). 'default' lets the CMake "
            "side resolve from +profiling (ON -> 1, OFF -> 0). Setting "
            "profiling_level=N implies +profiling unless ~profiling is "
            "also given, which forces level 0 (CMake kill switch)."
        ),
    )

    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+rocm", when="amdgpu_target=none")

    # Kokkos dependencies. SERIAL is always in the ship gate regardless of what
    # other backends are enabled, so it is required unconditionally.
    depends_on("kokkos +serial")
    depends_on("kokkos +threads", when="+threads")
    depends_on("kokkos +openmp", when="+openmp")

    # Cabana — only Cabana::Core is used (AoSoA/slice/deep_copy), no
    # grid/neighbor-search components needed.
    depends_on("cabana +mpi")

    depends_on("mpi")

    # Trilinos dependency
    # Tessera uses Trilinos for load balancing via Zoltan2 (Tessera_Zoltan2Balancer.hpp
    # is the only Trilinos consumer). The disabled packages keep the Trilinos build
    # minimal, mirroring the spack.yaml environments used to build Tessera's
    # dependents (Canopy) on NVIDIA and AMD systems.
    #
    # Only variants that still exist in current Trilinos may be named here.
    # Trilinos deprecated the Epetra stack in 17.0.0 and its spack package
    # guards those variants with `with when("@:16")`, so naming any of
    # ~amesos ~aztec ~epetra ~epetraext ~ifpack ~ml caps the whole DAG at
    # trilinos@14.2.0 -- which predates external-Kokkos support (@14.4:) and
    # therefore builds its own bundled Kokkos alongside the one Tessera uses.
    # Those packages are off by default in 17.0.0+, so dropping them from this
    # list changes nothing about what gets built.
    trilinos_base = (
        "+zoltan2 ~muelu ~ifpack2 ~fortran ~belos ~anasazi ~amesos2"
    )
    depends_on(f"trilinos {trilinos_base}")
    depends_on(f"trilinos {trilinos_base} +openmp", when="+openmp")

    # Trilinos GPU dependencies
    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on(f"trilinos {trilinos_base} {cuda_dep}", when=cuda_dep)

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on(f"trilinos {trilinos_base} {rocm_dep}", when=rocm_dep)

    # Cabana GPU dependencies
    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on(f"cabana {cuda_dep}", when=cuda_dep)

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on(f"cabana {rocm_dep}", when=rocm_dep)

    # I/O — Tessera's CMake hard-requires a parallel HDF5 build (FATAL_ERROR if
    # HDF5_IS_PARALLEL is false), so this is unconditional, not gated by a variant.
    depends_on("hdf5 +mpi")

    # If we're using CUDA or ROCM, require MPIs be GPU-aware
    conflicts("mpich ~cuda", when="+cuda")
    conflicts("mpich ~rocm", when="+rocm")
    conflicts("openmpi ~cuda", when="+cuda")
    conflicts("openmpi ~rocm", when="+rocm")

    # CMake specific build functions
    def cmake_args(self):
        options = []

        for var in ["TESTING", "EXAMPLES", "PROFILING"]:
            options.append(self.define_from_variant(f"Tessera_ENABLE_{var}", var.lower()))

        options.append(self.define_from_variant("Tessera_ENABLE_DEBUG_CHECKS", "debug"))

        # If testing is enabled, also install the tests
        options.append(self.define_from_variant("Tessera_INSTALL_TEST_EXECUTABLES", "testing"))

        # If examples are enabled, also install the examples
        options.append(self.define_from_variant("Tessera_INSTALL_EXAMPLES", "examples"))

        # profiling_level: pin a specific level if set, else let
        # Tessera_ENABLE_PROFILING alone drive it (ON -> 1, OFF -> 0).
        level = self.spec.variants["profiling_level"].value
        if level != "default":
            options.append(self.define("Tessera_PROFILING_LEVEL", level))

        return options

    def setup_run_environment(self, env):
        # +testing installs test binaries to share/Tessera/tests/. Spack only
        # puts bin/ on PATH by default, so prepend the tests dir so users can
        # invoke `tessera_test_<name>_<BACKEND>` after `spack env activate`.
        if self.spec.satisfies("+testing"):
            env.prepend_path("PATH", self.prefix.share.Tessera.tests)

    # ----------------------------------------------------------------------- #
    # Stand-alone tests (`spack test run tessera`, also `spack install
    # --test=root`).
    #
    # Scope: a single-rank SERIAL smoke test only. `spack test` runs on a login
    # node with no scheduler allocation, so multi-rank and GPU correctness (the
    # full minimum test set and device backends) cannot run here -- those are
    # validated in the build tree with `ctest` via the per-system batch scripts
    # (see docs/<system>/claude.md and scripts/<system>/). The "keys" unit test
    # exercises both the host (Serial) and device (Kokkos default execution
    # space) code paths from a single binary, so even the SERIAL-named binary
    # brings up the GPU backend on a +cuda/+rocm build -- which needs an
    # allocation `spack test` does not hold on a login node.
    # ----------------------------------------------------------------------- #
    def test_keys_serial(self):
        """run the SERIAL keys unit test at a single rank"""
        if self.spec.satisfies("~testing"):
            raise SkipTest("test binaries are only installed with +testing")
        if self.spec.satisfies("+cuda") or self.spec.satisfies("+rocm"):
            raise SkipTest(
                "GPU build: run tests via the scheduler batch scripts "
                "(docs/<system>/claude.md), not `spack test`"
            )

        exe = which(
            "tessera_test_keys_SERIAL",
            path=self.prefix.share.Tessera.tests,
            required=True,
        )
        # Invoked directly => singleton MPI rank (np=1); no launcher needed.
        with test_part(
            self,
            "test_keys_serial",
            purpose="single-rank SERIAL keys smoke test",
        ):
            exe()
