# Run manifest: 2026-11-23-tuolumne-compute-check

- **Commit:** `8db460b4abb2f0e195c3695961ad19b67ce33a27` on `conditional-system-config`
- **Host:** `tuolumne2152`
- **Started:** 2026-11-23T20:52:03Z
- **Elapsed:** 102 s
- **Exit status of run.sh:** 0
- **Spack:** `1.2.2 (3e19345b6e12f5ff1b874f4059622fc6a1fd804a)`

## Environment

```
CRAY_BINUTILS_BIN_AARCH64=/opt/cray/pe/cce/20.0.0/binutils/cross/x86_64-aarch64/aarch64-linux-gnu/bin
CRAY_BINUTILS_BIN=/opt/cray/pe/cce/20.0.0/binutils/x86_64/bin
CRAY_BINUTILS_BIN_X86_64=/opt/cray/pe/cce/20.0.0/binutils/x86_64/bin
CRAY_BINUTILS_ROOT_AARCH64=/opt/cray/pe/cce/20.0.0/binutils/cross/x86_64-aarch64/aarch64-linux-gnu/../
CRAY_BINUTILS_ROOT=/opt/cray/pe/cce/20.0.0/binutils/x86_64/x86_64-pc-linux-gnu/../
CRAY_BINUTILS_ROOT_X86_64=/opt/cray/pe/cce/20.0.0/binutils/x86_64/x86_64-pc-linux-gnu/../
CRAY_BINUTILS_VERSION=/opt/cray/pe/cce/20.0.0
CRAY_CCE_CLANGSHARE=/opt/cray/pe/cce/20.0.0/cce-clang/x86_64/share
CRAY_CCE_SHARE=/opt/cray/pe/cce/20.0.0/cce/x86_64/share
CRAY_CC_VERSION=20.0.0
CRAY_CPU_TARGET=x86-trento
CRAY_CXX_IPA_LIBS_AARCH64=/opt/cray/pe/cce/20.0.0/cce/aarch64/lib/libcray-c++-rts.a
CRAY_CXX_IPA_LIBS=/opt/cray/pe/cce/20.0.0/cce/x86_64/lib/libcray-c++-rts.a
CRAY_CXX_IPA_LIBS_X86_64=/opt/cray/pe/cce/20.0.0/cce/x86_64/lib/libcray-c++-rts.a
CRAY_FTN_VERSION=20.0.0
CRAY_LD_LIBRARY_PATH=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0/lib:/opt/cray/pe/mpich/9.0.1/gtl/lib:/opt/cray/pe/libsci/25.09.0/CRAYCLANG/20.0/x86_64/lib:/opt/cray/pe/cce/20.0.0/cce-clang/x86_64/lib:/opt/cray/pe/cce/20.0.0/cce/x86_64/lib:/opt/cray/pe/lib64:/opt/cray/lib64:/opt/cray/pe/perftools/25.09.0/lib64
CRAY_LIBSCI_BASE_DIR=/opt/cray/pe/libsci/25.09.0
CRAY_LIBSCI_PREFIX_DIR=/opt/cray/pe/libsci/25.09.0/CRAYCLANG/20.0/x86_64
CRAY_LIBSCI_PREFIX=/opt/cray/pe/libsci/25.09.0/CRAYCLANG/20.0/x86_64
CRAY_LIBSCI_VERSION=25.09.0
CRAY_LMOD_COMPILER=crayclang/20.0
CRAY_LMOD_CPU=x86-trento/1.0
CRAY_LMOD_MPI=cray-mpich/8.0
CRAY_LMOD_NET=ofi/1.0
CRAY_MPICH_BASEDIR=/opt/cray/pe/mpich/9.0.1/ofi
CRAY_MPICH_DIR=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0
CRAY_MPICH_PREFIX=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0
CRAY_MPICH_ROOTDIR=/opt/cray/pe/mpich/9.0.1
CRAY_MPICH_VER=9.0.1
CRAY_MPICH_VERSION=9.0.1
CRAY_PE_CCE_VARIANT=CC=Clang:FTN=Classic
CRAY_PERFTOOLS_PREFIX=/opt/cray/pe/perftools/25.09.0
CRAY_PERFTOOLS_VERSION=25.09.0
CRAY_PE_USE_CLANG=/opt/cray/pe/cce/20.0.0/cce-clang/x86_64/bin/clang
FLUX_F58_FORCE_ASCII=t
HSA_ENABLE_IPC_MODE_LEGACY=1
LD_LIBRARY_PATH=/opt/cray/pe/lib64:/opt/cray/lib64:/opt/cray/pe/papi/7.2.0.2/lib64
LOADEDMODULES=craype-x86-trento:libfabric/match_SHS:craype-network-ofi:perftools-base/25.09.0:craype/2.7.35:PrgEnv-cray/8.7.0:flux_wrappers/0.1:xpmem/2.6.5:StdEnv:cce/20.0.0:cray-libsci/25.09.0:cray-mpich/9.0.1
MPICH_DIR=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0
MPICH_LOCAL_SPAWN_SERVER=0
PE_CRAYCLANG_FIXED_PKGCONFIG_PATH=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0/lib/pkgconfig
PE_ENV=CRAY
PE_FORTRAN_PKGCONFIG_LIBS=mpichf90
PE_LEVEL=20.0
PE_LIBSCI_GENCOMPILERS_CRAYCLANG_x86_64=20.0
PE_LIBSCI_GENCOMPS_CRAYCLANG_x86_64=200
PE_LIBSCI_MODULE_NAME=cray-libsci/25.09.0
PE_LIBSCI_OMP_REQUIRES= 
PE_LIBSCI_OMP_REQUIRES_openmp=_mp
PE_LIBSCI_PKGCONFIG_LIBS=libsci_mpi:libsci
PE_LIBSCI_PKGCONFIG_VARIABLES=PE_LIBSCI_OMP_REQUIRES_@openmp@:PE_SCI_EXT_LIBPATH:PE_SCI_EXT_LIBNAME
PE_LIBSCI_REQUIRED_PRODUCTS=PE_MPICH
PE_LIBSCI_VOLATILE_PKGCONFIG_PATH=/opt/cray/pe/libsci/25.09.0/@PRGENV@/@PE_LIBSCI_GENCOMPS@/@PE_LIBSCI_TARGET@/lib/pkgconfig
PE_LIBSCI_VOLATILE_PRGENV=CRAYCLANG
PE_MPICH_FIXED_PRGENV=CRAYCLANG
PE_MPICH_FORTRAN_PKGCONFIG_LIBS=mpichf90
PE_MPICH_GENCOMPILERS_CRAYCLANG=20.0
PE_MPICH_GTL_DIR_amd_gfx906=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_amd_gfx908=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_amd_gfx90a=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_amd_gfx940=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_amd_gfx942=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_nvidia70=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_nvidia80=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_nvidia90=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_DIR_ponteVecchio=-L/opt/cray/pe/mpich/9.0.1/gtl/lib
PE_MPICH_GTL_LIBS_amd_gfx906=-lmpi_gtl_hsa
PE_MPICH_GTL_LIBS_amd_gfx908=-lmpi_gtl_hsa
PE_MPICH_GTL_LIBS_amd_gfx90a=-lmpi_gtl_hsa
PE_MPICH_GTL_LIBS_amd_gfx940=-lmpi_gtl_hsa
PE_MPICH_GTL_LIBS_amd_gfx942=-lmpi_gtl_hsa
PE_MPICH_GTL_LIBS_nvidia70=-lmpi_gtl_cuda
PE_MPICH_GTL_LIBS_nvidia80=-lmpi_gtl_cuda
PE_MPICH_GTL_LIBS_nvidia90=-lmpi_gtl_cuda
PE_MPICH_GTL_LIBS_ponteVecchio=-lmpi_gtl_ze
PE_MPICH_MODULE_NAME=cray-mpich
PE_MPICH_PKGCONFIG_LIBS=mpich
PE_MPICH_PKGCONFIG_VARIABLES=PE_MPICH_GTL_DIR_@accelerator@:PE_MPICH_GTL_LIBS_@accelerator@
PE_PERFTOOLS_MPICH_LIBDIR=/opt/cray/pe/mpich/9.0.1/ofi/crayclang/20.0/lib
PE_PKGCONFIG_LIBS=mpich:libsci_mpi:libsci
PE_PKGCONFIG_PRODUCTS=PE_MPICH:PE_LIBSCI:PE_XPMEM
PE_PRODUCT_LIST=CRAYPE:CRAYPE_X86_TRENTO:PERFTOOLS:CRAYPAT
PE_XPMEM_PKGCONFIG_LIBS=xpmem
SPACK_PYTHON=/usr/tce/bin/python3
SPACK_ROOT=/g/g16/bridges7/spack
SPACK_USER_CONFIG_PATH=/g/g16/bridges7/.spack/tuolumne
```
