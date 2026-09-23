def register_backend_for_device(
    device: str,
    device_scheduling: SchedulingConstructor,
    device_wrapper_codegen: WrapperConstructor,
    device_cpp_wrapper_codegen: Optional[WrapperConstructor] = None,
    device_custom_pass: Optional[CustomGraphModulePass] = None,
) -> None:
    device_codegens[device] = DeviceCodegen(
        device_scheduling, device_wrapper_codegen, device_cpp_wrapper_codegen
    )
    custom_backend_passes[device] = device_custom_pass
