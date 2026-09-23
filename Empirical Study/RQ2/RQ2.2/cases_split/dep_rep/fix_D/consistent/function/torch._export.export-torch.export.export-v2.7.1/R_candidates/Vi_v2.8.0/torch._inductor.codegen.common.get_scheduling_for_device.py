def get_scheduling_for_device(device: str) -> Optional[SchedulingConstructor]:
    return device_codegens[device].scheduling if device in device_codegens else None
