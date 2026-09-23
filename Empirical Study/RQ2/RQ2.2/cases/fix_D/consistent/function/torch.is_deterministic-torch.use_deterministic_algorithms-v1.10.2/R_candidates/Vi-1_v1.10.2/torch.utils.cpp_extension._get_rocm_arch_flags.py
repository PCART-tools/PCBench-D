def _get_rocm_arch_flags(cflags: Optional[List[str]] = None) -> List[str]:
    # If cflags is given, there may already be user-provided arch flags in it
    # (from `extra_compile_args`)
    if cflags is not None:
        for flag in cflags:
            if 'amdgpu-target' in flag:
                return ['-fno-gpu-rdc']
    # Use same defaults from file cmake/public/LoadHIP.cmake.
    # Must keep in sync if defaults change.
    # Allow env var to override, just like during initial cmake build.
    archs = os.environ.get('PYTORCH_ROCM_ARCH', 'gfx803;gfx900;gfx906;gfx908')
    flags = ['--amdgpu-target=%s' % arch for arch in archs.split(';')]
    flags += ['-fno-gpu-rdc']
    return flags
