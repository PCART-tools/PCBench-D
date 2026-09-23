def _get_rocm_arch_flags(cflags: Optional[List[str]] = None) -> List[str]:
    # If cflags is given, there may already be user-provided arch flags in it
    # (from `extra_compile_args`)
    if cflags is not None:
        for flag in cflags:
            if 'amdgpu-target' in flag:
                return ['-fno-gpu-rdc']
    # Use same defaults as used for building PyTorch
    # Allow env var to override, just like during initial cmake build.
    _archs = os.environ.get('PYTORCH_ROCM_ARCH', None)
    if not _archs:
        archs = torch.cuda.get_arch_list()
    else:
        archs = _archs.replace(' ', ';').split(';')
    flags = ['--amdgpu-target=%s' % arch for arch in archs]
    flags += ['-fno-gpu-rdc']
    return flags
