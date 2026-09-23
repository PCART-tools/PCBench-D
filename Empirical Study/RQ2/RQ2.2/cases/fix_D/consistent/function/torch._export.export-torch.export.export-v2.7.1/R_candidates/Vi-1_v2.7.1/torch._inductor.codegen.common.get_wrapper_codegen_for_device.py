def get_wrapper_codegen_for_device(
    device: str, cpp_wrapper: bool = False
) -> Optional[WrapperConstructor]:
    if device in device_codegens:
        wrapper_codegen_obj: DeviceCodegen = device_codegens[device]
        return (
            wrapper_codegen_obj.cpp_wrapper_codegen
            if cpp_wrapper
            else wrapper_codegen_obj.wrapper_codegen
        )
    return None
