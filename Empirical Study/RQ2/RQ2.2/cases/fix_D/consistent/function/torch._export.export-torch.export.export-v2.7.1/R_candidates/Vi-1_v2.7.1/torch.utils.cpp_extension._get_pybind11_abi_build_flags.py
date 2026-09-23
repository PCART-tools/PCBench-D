def _get_pybind11_abi_build_flags():
    # Note [Pybind11 ABI constants]
    #
    # Pybind11 before 2.4 used to build an ABI strings using the following pattern:
    # f"__pybind11_internals_v{PYBIND11_INTERNALS_VERSION}{PYBIND11_INTERNALS_KIND}{PYBIND11_BUILD_TYPE}__"
    # Since 2.4 compier type, stdlib and build abi parameters are also encoded like this:
    # f"__pybind11_internals_v{PYBIND11_INTERNALS_VERSION}{PYBIND11_INTERNALS_KIND}{PYBIND11_COMPILER_TYPE}{PYBIND11_STDLIB}{PYBIND11_BUILD_ABI}{PYBIND11_BUILD_TYPE}__"
    #
    # This was done in order to further narrow down the chances of compiler ABI incompatibility
    # that can cause a hard to debug segfaults.
    # For PyTorch extensions we want to relax those restrictions and pass compiler, stdlib and abi properties
    # captured during PyTorch native library compilation in torch/csrc/Module.cpp

    abi_cflags = []
    for pname in ["COMPILER_TYPE", "STDLIB", "BUILD_ABI"]:
        pval = getattr(torch._C, f"_PYBIND11_{pname}")
        if pval is not None and not IS_WINDOWS:
            abi_cflags.append(f'-DPYBIND11_{pname}=\\"{pval}\\"')
    return abi_cflags
