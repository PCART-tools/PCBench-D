def _raw_device_uuid_amdsmi() -> Optional[list[str]]:
    from ctypes import byref, c_int, c_void_p, CDLL, create_string_buffer

    if not _HAS_PYNVML:  # If amdsmi is not available
        return None
    try:
        amdsmi.amdsmi_init()
    except amdsmi.AmdSmiException:
        warnings.warn("Can't initialize amdsmi")
        return None
    try:
        socket_handles = amdsmi.amdsmi_get_processor_handles()
        dev_count = len(socket_handles)
    except amdsmi.AmdSmiException:
        warnings.warn("Can't get amdsmi device count")
        return None
    uuids: list[str] = []
    for idx in range(dev_count):
        try:
            handler = amdsmi.amdsmi_get_processor_handles()[idx]
        except amdsmi.AmdSmiException:
            warnings.warn("Cannot get amd device handler")
            return None
        try:
            uuid = amdsmi.amdsmi_get_gpu_asic_info(handler)["asic_serial"][
                2:
            ]  # Removes 0x prefix from serial
        except amdsmi.AmdSmiException:
            warnings.warn("Cannot get uuid for amd device")
            return None
        uuids.append(
            str(uuid).lower()
        )  # Lower-case to match expected HIP_VISIBLE_DEVICES uuid input
    return uuids
