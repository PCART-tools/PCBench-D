def _get_amdsmi_memory_usage(device: Optional[Union[Device, int]] = None) -> int:
    handle = _get_amdsmi_handler()
    device = _get_amdsmi_device_index(device)
    handle = amdsmi.amdsmi_get_processor_handles()[device]
    return amdsmi.amdsmi_get_gpu_activity(handle)["umc_activity"]
