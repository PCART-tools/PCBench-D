def set_flags(_enabled=None, _benchmark=None, _deterministic=None, _allow_tf32=None):
    orig_flags = (torch._C._get_cudnn_enabled(),
                  torch._C._get_cudnn_benchmark(),
                  torch._C._get_cudnn_deterministic(),
                  torch._C._get_cudnn_allow_tf32())
    if _enabled is not None:
        torch._C._set_cudnn_enabled(_enabled)
    if _benchmark is not None:
        torch._C._set_cudnn_benchmark(_benchmark)
    if _deterministic is not None:
        torch._C._set_cudnn_deterministic(_deterministic)
    if _allow_tf32 is not None:
        torch._C._set_cudnn_allow_tf32(_allow_tf32)
    return orig_flags
