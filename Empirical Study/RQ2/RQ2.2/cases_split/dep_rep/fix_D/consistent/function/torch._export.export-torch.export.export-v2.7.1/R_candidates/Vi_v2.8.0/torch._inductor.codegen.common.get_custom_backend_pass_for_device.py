def get_custom_backend_pass_for_device(device: str) -> Optional[CustomGraphModulePass]:
    return custom_backend_passes[device] if device in custom_backend_passes else None
