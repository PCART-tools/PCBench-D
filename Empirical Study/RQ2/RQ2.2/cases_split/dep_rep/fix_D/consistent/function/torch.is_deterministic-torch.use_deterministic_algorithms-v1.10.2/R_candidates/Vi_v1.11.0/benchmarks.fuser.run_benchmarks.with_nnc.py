def with_nnc():
    torch._C._jit_override_can_fuse_on_cpu(True)
    torch._C._jit_override_can_fuse_on_gpu(True)
    torch._C._jit_set_texpr_fuser_enabled(True)
    torch._C._jit_set_nvfuser_enabled(False)
    torch._C._jit_set_profiling_executor(True)
    torch._C._jit_set_profiling_mode(True)
