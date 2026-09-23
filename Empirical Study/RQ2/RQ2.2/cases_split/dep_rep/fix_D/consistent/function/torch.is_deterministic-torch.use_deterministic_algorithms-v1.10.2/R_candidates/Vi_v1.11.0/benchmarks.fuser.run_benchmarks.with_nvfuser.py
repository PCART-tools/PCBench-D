def with_nvfuser():
    torch._C._jit_override_can_fuse_on_cpu(False)
    torch._C._jit_override_can_fuse_on_gpu(False)
    torch._C._jit_set_texpr_fuser_enabled(False)
    torch._C._jit_set_nvfuser_enabled(True)
    torch._C._jit_set_profiling_executor(True)
    torch._C._jit_set_profiling_mode(True)
