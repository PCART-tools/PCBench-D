def _get_rocm_arch_flags(cflags: Optional[list[str]] = None) -> list[str]:
    # If cflags is given, there may already be user-provided arch flags in it
    # (from `extra_compile_args`)
    if cflags is not None:
        for flag in cflags:
            if 'amdgpu-target' in flag or 'offload-arch' in flag:
                return ['-fno-gpu-rdc']
    # Use same defaults as used for building PyTorch
    # Allow env var to override, just like during initial cmake build.
    _archs = os.environ.get('PYTORCH_ROCM_ARCH', None)
    if not _archs:
        archFlags = torch._C._cuda_getArchFlags()
        if archFlags:
            archs = archFlags.split()
        else:
            archs = []
    else:
        archs = _archs.replace(' ', ';').split(';')
    flags = [f'--offload-arch={arch}' for arch in archs]
    flags += ['-fno-gpu-rdc']
    return flags
