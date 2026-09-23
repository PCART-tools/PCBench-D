def register_backend_for_device(
    device: str,
    device_scheduling: SchedulingConstructor,
    device_wrapper_codegen: WrapperConstructor,
    device_cpp_wrapper_codegen: Optional[WrapperConstructor] = None,
) -> None:
    device_codegens[device] = DeviceCodegen(
        device_scheduling, device_wrapper_codegen, device_cpp_wrapper_codegen
    )
