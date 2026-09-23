@functools.lru_cache(None)
def init_backend_registration() -> None:
    from .cpp import CppScheduling
    from .cpp_wrapper_cpu import CppWrapperCpu
    from .cpp_wrapper_cpu_array_ref import CppWrapperCpuArrayRef
    from .cpp_wrapper_gpu import CppWrapperGpu
    from .cuda_combined_scheduling import CUDACombinedScheduling
    from .halide import HalideScheduling
    from .mps import MetalScheduling
    from .triton import TritonScheduling
    from .wrapper import PythonWrapperCodegen

    if get_scheduling_for_device("cpu") is None:
        cpu_backends = {
            "cpp": CppScheduling,
            "halide": HalideScheduling,
            "triton": TritonScheduling,
        }
        register_backend_for_device(
            "cpu",
            lambda scheduling: cpu_backends[config.cpu_backend](scheduling),
            PythonWrapperCodegen,
            CppWrapperCpuArrayRef
            if config.aot_inductor.allow_stack_allocation
            else CppWrapperCpu,
        )

    if get_scheduling_for_device("cuda") is None:
        # CUDACombinedScheduling combines Triton and CUDA C++ scheduling for CUDA devices via delegation
        cuda_backends = {
            "triton": CUDACombinedScheduling,
            "halide": HalideScheduling,
        }
        register_backend_for_device(
            "cuda",
            lambda scheduling: cuda_backends[config.cuda_backend](scheduling),
            PythonWrapperCodegen,
            CppWrapperGpu,
        )

    if get_scheduling_for_device("xpu") is None:
        register_backend_for_device(
            "xpu",
            TritonScheduling,
            PythonWrapperCodegen,
            CppWrapperGpu,
        )

    if get_scheduling_for_device("mps") is None:
        register_backend_for_device(
            "mps",
            MetalScheduling,
            PythonWrapperCodegen,
            CppWrapperGpu,
        )

    private_backend = torch._C._get_privateuse1_backend_name()
    if (
        private_backend != "privateuseone"
        and get_scheduling_for_device(private_backend) is None
    ):
        from torch.utils.backend_registration import _get_custom_mod_func

        try:
            device_scheduling = _get_custom_mod_func("Scheduling")
            wrapper_codegen = _get_custom_mod_func("PythonWrapperCodegen")
            cpp_wrapper_codegen = _get_custom_mod_func("CppWrapperCodegen")
            if device_scheduling and wrapper_codegen and cpp_wrapper_codegen:
                register_backend_for_device(
                    private_backend,
                    device_scheduling,
                    wrapper_codegen,
                    cpp_wrapper_codegen,
                )
        except RuntimeError:
            pass
