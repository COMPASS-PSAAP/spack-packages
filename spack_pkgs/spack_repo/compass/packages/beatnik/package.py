# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class Beatnik(CMakePackage, CudaPackage, ROCmPackage):
    """Fluid interface model solver based on Pandya and Shkoller's Z-Model formulation."""

    homepage = "https://github.com/CUP-ECS/beatnik"
    git = "https://github.com/CUP-ECS/beatnik.git"

    maintainers("patrickb314", "JStewart28")

    license("BSD-3-Clause")

    version("1.1", commit="7d5a6fa588bcb7065fc53c3e8ae52d4d7f13b6f1", submodules=True)
    version("1.0", commit="ae31ef9cb44678d5ace77994b45b0778defa3d2f")
    version("develop", branch="develop", submodules=True)
    version("main", branch="main", submodules=True)

    # Variants are primarily backends to build on GPU systems and pass the right
    # informtion to the packages we depend on
    variant("cuda", default=False, description="Use CUDA support from subpackages")
    variant("openmp", default=False, description="Use OpenMP support from subpackages")
    variant(
        "canopy",
        default=False,
        description="Enable the FMM-based BR solver backed by Canopy (-S fmm)",
    )
    variant(
        "testing",
        default=False,
        description="Build the Beatnik test suite (Beatnik_ENABLE_TESTING=ON; requires GTest)",
    )
    variant(
        "examples",
        default=True,
        description="Build and install the Beatnik example binaries (rocketrig)",
    )
    variant(
        "profiling",
        default=False,
        description="Enable Beatnik profiling/diagnostics instrumentation",
    )
    variant(
        "profiling_level",
        default="default",
        values=("default", "0", "1", "2", "3"),
        multi=False,
        description=(
            "Profiling detail level: 0=off, 1=basic (auto_maintain action "
            "log), 2/3=detailed/verbose (reserved). 'default' lets the "
            "CMake side resolve from +profiling (ON -> 1, OFF -> 0). "
            "Setting profiling_level=N implies +profiling unless ~profiling "
            "is also given, which forces level 0 (CMake kill switch)."
        ),
    )

    # Dependencies for all Beatnik versions
    depends_on("c", type="build")
    depends_on("cxx", type="build")  # generated

    depends_on("mpi")
    with when("+cuda"):
        depends_on("mpich +cuda", when="^[virtuals=mpi] mpich")
        depends_on("mvapich-plus +cuda", when="^[virtuals=mpi] mvapich-plus")
        depends_on("openmpi +cuda", when="^[virtuals=mpi] openmpi")

    with when("+rocm"):
        depends_on("mpich +rocm", when="^[virtuals=mpi] mpich")
        depends_on("mvapich-plus +rocm", when="^[virtuals=mpi] mvapich-plus")
        depends_on("openmpi +rocm", when="^[virtuals=mpi] openmpi@5:")

    # Kokkos dependencies
    depends_on("kokkos @4:")
    depends_on("kokkos +cuda +cuda_lambda +cuda_constexpr", when="+cuda")
    depends_on("kokkos +rocm", when="+rocm")
    depends_on("kokkos +wrapper", when="+cuda%gcc")

    # Cabana dependencies
    depends_on("cabana @0.7.0 +grid +heffte +silo +hdf5 +mpi +arborx", when="@1.1")
    depends_on("cabana @0.7.0 +grid +heffte +silo +hdf5 +mpi +arborx", when="@1.0")
    depends_on("cabana @master +grid +heffte +silo +hdf5 +mpi +arborx", when="@develop")
    depends_on("cabana @0.7.0 +grid +heffte +silo +hdf5 +mpi +arborx", when="@main")
    depends_on("cabana +cuda", when="+cuda")
    depends_on("cabana +rocm", when="+rocm")

    # Silo dependencies
    depends_on("silo @4.11: ~fpzip~hzip~python~hdf5")
    depends_on("silo @4.11.1 ~fpzip~hzip~python~hdf5", when="%cce")
    # Eariler silo versions have trouble with cce

    # Heffte dependencies - We always require FFTW so that there's a host
    # backend even when we're compiling for GPUs
    depends_on("heffte +fftw")
    depends_on("heffte +cuda", when="+cuda")
    depends_on("heffte +rocm", when="+rocm")

    # If we're using CUDA or ROCM, require MPIs be GPU-aware
    conflicts("mpich ~cuda", when="+cuda")
    conflicts("mpich ~rocm", when="+rocm")
    conflicts("openmpi ~cuda", when="+cuda")
    # Heffte won't build with intel MPI because of needed C++ MPI support
    conflicts("^intel-oneapi-mpi")
    conflicts("^spectrum-mpi", when="^cuda@11.3:")  # cuda-aware spectrum is broken with cuda 11.3:

    # Propagate CUDA and AMD GPU targets to cabana
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on("cabana cuda_arch=%s" % cuda_arch, when="+cuda cuda_arch=%s" % cuda_arch)
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "cabana +rocm amdgpu_target=%s" % amdgpu_value,
            when="+rocm amdgpu_target=%s" % amdgpu_value,
        )

    # Canopy FMM solver (optional). Propagate the GPU target so Canopy
    # builds for the same arch as the rest of the stack.
    depends_on("canopy", when="+canopy")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "canopy cuda_arch=%s" % cuda_arch,
            when="+canopy +cuda cuda_arch=%s" % cuda_arch,
        )
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "canopy +rocm amdgpu_target=%s" % amdgpu_value,
            when="+canopy +rocm amdgpu_target=%s" % amdgpu_value,
        )

    # GTest is required by the Beatnik test harness when +testing is enabled.
    depends_on("googletest @1.10:", when="+testing")

    # CMake specific build functions
    def cmake_args(self):
        args = []

        # Use hipcc as the c compiler if we are compiling for rocm. Doing it this way
        # keeps the wrapper insted of changeing CMAKE_CXX_COMPILER keeps the spack wrapper
        # and the rpaths it sets for us from the underlying spec.
        if self.spec.satisfies("+rocm"):
            env["SPACK_CXX"] = self.spec["hip"].hipcc

        # If we're building with cray mpich, we need to make sure we get the GTL library for
        # gpu-aware MPI, since cabana and beatnik require it
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

        # Optional Canopy FMM solver. When +canopy, force the find_package to
        # succeed so the build fails fast if Canopy is missing.
        args.append(self.define_from_variant("Beatnik_REQUIRE_CANOPY", "canopy"))

        # Test suite (off by default; Beatnik's top-level CMakeLists.txt also
        # defaults it OFF, but be explicit so the variant is single-source).
        # +testing also flips INSTALL_TEST_EXECUTABLES so the per-device test
        # binaries land in the spack prefix (under share/Beatnik/tests/, per
        # the test harness convention — NOT in bin/).
        args.append(self.define_from_variant("Beatnik_ENABLE_TESTING", "testing"))
        args.append(self.define_from_variant("Beatnik_INSTALL_TEST_EXECUTABLES", "testing"))

        # Examples (rocketrig). +examples flips both ENABLE and INSTALL on so
        # the binary is built AND installed into the spack prefix's bin/.
        # Beatnik's top-level CMakeLists.txt defaults both OFF to mirror
        # Canopy_ENABLE_EXAMPLES / Canopy_INSTALL_EXAMPLES.
        args.append(self.define_from_variant("Beatnik_ENABLE_EXAMPLES", "examples"))
        args.append(self.define_from_variant("Beatnik_INSTALL_EXAMPLES", "examples"))

        # Profiling. +profiling is the kill switch; profiling_level lets the
        # spec pin a specific level (0/1/2/3) directly. "default" passes the
        # empty string to CMake so Beatnik's CMakeLists.txt picks the level
        # from Beatnik_ENABLE_PROFILING alone (ON -> 1, OFF -> 0).
        args.append(self.define_from_variant("Beatnik_ENABLE_PROFILING", "profiling"))
        level = self.spec.variants["profiling_level"].value
        if level != "default":
            args.append(self.define("Beatnik_PROFILING_LEVEL", level))

        return args

    def setup_run_environment(self, env):
        # +testing installs test binaries to share/Beatnik/tests/ (per the
        # test_harness.cmake convention). Spack only puts bin/ on PATH by
        # default, so prepend the tests dir so users can invoke
        # `Beatnik_Test_FmmVsExact_MPI_<DEVICE>` after `spack env activate`.
        if self.spec.satisfies("+testing"):
            env.prepend_path("PATH", self.prefix.share.Beatnik.tests)
