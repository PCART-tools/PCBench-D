def is_noncontiguous_supported(device):
    return device is None or device.type != "hpu"
