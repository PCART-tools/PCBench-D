def _nvrtc_compile(
    kernel_source: str,
    kernel_name: str,
    compute_capability: Optional[str] = None,
    header_code: str = "",
    cuda_include_dirs: Optional[list] = None,
    nvcc_options: Optional[list] = None,
) -> bytes:
    """
    Compiles a CUDA kernel using NVRTC and returns the PTX code.

    Args:
        kernel_source (str): The CUDA kernel source code as a string
        kernel_name (str): The name of the kernel function to compile
        compute_capability (str, None): The compute capability to target (e.g., "86").
                                           If None, will detect from current device.
        header_code (str, optional): Additional header code to prepend to the kernel source
        cuda_include_dirs (list, None): List of directories containing CUDA headers
        nvcc_options (list, None): Additional options to pass to NVRTC

    Returns:
        str: The compiled PTX code
    """
    # Ensure CUDA is initialized
    import torch.cuda

    # Load NVRTC library
    libnvrtc = _get_nvrtc_library()

    # NVRTC constants
    NVRTC_SUCCESS = 0

    # Helper: check NVRTC errors
    def check_nvrtc(result: int) -> None:
        if result != NVRTC_SUCCESS:
            err_str = ctypes.c_char_p()
            libnvrtc.nvrtcGetErrorString(result, ctypes.byref(err_str))
            error_message = (
                err_str.value.decode()
                if err_str.value is not None
                else "Unknown CUDA error"
            )
            raise RuntimeError(f"CUDA error: {error_message}")

    # Add 'extern "C"' if not already present to ensure C linkage
    if not kernel_source.strip().startswith('extern "C"'):
        kernel_source = f'extern "C" {kernel_source}'

    # Combine header code and kernel source
    if header_code:
        full_source = header_code + "\n" + kernel_source
    else:
        full_source = kernel_source

    # Convert source to bytes
    source_bytes = full_source.encode("utf-8")

    # Get compute capability if not provided
    if compute_capability is None:
        props = torch.cuda.get_device_properties(torch.cuda.current_device())
        compute_capability = f"{props.major}{props.minor}"

    # Prepare compilation options
    options = []
    options.append(f"--gpu-architecture=sm_{compute_capability}".encode())

    # Add custom include directories
    if cuda_include_dirs:
        for directory in cuda_include_dirs:
            options.append(f"-I{directory}".encode())

    # Add custom NVCC options
    if nvcc_options:
        for option in nvcc_options:
            options.append(option.encode("utf-8"))

    # TODO: Should we refactor flags into a common place?
    from torch.utils.cpp_extension import COMMON_NVCC_FLAGS

    # Filter out flags not supported by NVRTC
    nvrtc_compatible_flags = [
        flag for flag in COMMON_NVCC_FLAGS if flag != "--expt-relaxed-constexpr"
    ]
    options.extend([flag.encode("utf-8") for flag in nvrtc_compatible_flags])

    # Convert options to C array
    num_options = len(options)
    options_array = (ctypes.c_char_p * num_options)(*options)

    # Create program
    prog = ctypes.c_void_p()
    check_nvrtc(
        libnvrtc.nvrtcCreateProgram(
            ctypes.byref(prog),
            source_bytes,
            f"{kernel_name}.cu".encode(),
            0,
            None,
            None,
        )
    )

    # Compile program
    res = libnvrtc.nvrtcCompileProgram(prog, num_options, options_array)

    # Handle compilation errors
    if res != NVRTC_SUCCESS:
        # Get log
        log_size = ctypes.c_size_t()
        libnvrtc.nvrtcGetProgramLogSize(prog, ctypes.byref(log_size))
        log = ctypes.create_string_buffer(log_size.value)
        libnvrtc.nvrtcGetProgramLog(prog, log)
        raise RuntimeError(f"Kernel compilation failed:\n{log.value.decode()}")

    # Get PTX
    ptx_size = ctypes.c_size_t()
    check_nvrtc(libnvrtc.nvrtcGetPTXSize(prog, ctypes.byref(ptx_size)))
    ptx = ctypes.create_string_buffer(ptx_size.value)
    check_nvrtc(libnvrtc.nvrtcGetPTX(prog, ptx))
    libnvrtc.nvrtcDestroyProgram(ctypes.byref(prog))

    return ptx.value
