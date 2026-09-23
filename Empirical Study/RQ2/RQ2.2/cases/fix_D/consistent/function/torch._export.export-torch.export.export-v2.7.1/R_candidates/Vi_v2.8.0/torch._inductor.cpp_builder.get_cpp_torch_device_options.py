def get_cpp_torch_device_options(
    device_type: str,
    aot_mode: bool = False,
    compile_only: bool = False,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    definitions: list[str] = []
    include_dirs: list[str] = []
    cflags: list[str] = []
    ldflags: list[str] = []
    libraries_dirs: list[str] = []
    libraries: list[str] = []
    passthrough_args: list[str] = []
    if (
        config.is_fbcode()
        and "CUDA_HOME" not in os.environ
        and "CUDA_PATH" not in os.environ
    ):
        os.environ["CUDA_HOME"] = build_paths.sdk_home

    _set_gpu_runtime_env()
    from torch.utils import cpp_extension

    include_dirs = cpp_extension.include_paths(device_type)
    libraries_dirs = cpp_extension.library_paths(device_type)
    if device_type == "cuda":
        definitions.append(" USE_ROCM" if torch.version.hip else " USE_CUDA")

        if torch.version.hip is not None:
            if config.is_fbcode():
                libraries += ["amdhip64"]
            else:
                libraries += ["c10_hip", "torch_hip"]
            definitions.append(" __HIP_PLATFORM_AMD__")
        else:
            if config.is_fbcode():
                libraries += ["cuda"]
            else:
                libraries += ["c10_cuda", "cuda", "torch_cuda"]
            _transform_cuda_paths(libraries_dirs)

    if device_type == "xpu":
        definitions.append(" USE_XPU")
        # Suppress multi-line comment warnings in sycl headers
        cflags += ["Wno-comment"]
        libraries += ["c10_xpu", "sycl", "ze_loader", "torch_xpu"]
        if not find_library("ze_loader"):
            raise OSError(
                "Intel GPU driver is not properly installed, please follow the instruction "
                "in https://github.com/pytorch/pytorch?tab=readme-ov-file#intel-gpu-support."
            )

    if device_type == "mps":
        definitions.append(" USE_MPS")

    if config.is_fbcode():
        include_dirs.append(build_paths.sdk_include)

        if aot_mode and device_type == "cuda":
            if torch.version.hip is None:
                if not compile_only:
                    # Only add link args, when compile_only is false.
                    passthrough_args = ["-Wl,-Bstatic -lcudart_static -Wl,-Bdynamic"]

    if config.aot_inductor.custom_op_libs:
        libraries += config.aot_inductor.custom_op_libs

    return (
        definitions,
        include_dirs,
        cflags,
        ldflags,
        libraries_dirs,
        libraries,
        passthrough_args,
    )
