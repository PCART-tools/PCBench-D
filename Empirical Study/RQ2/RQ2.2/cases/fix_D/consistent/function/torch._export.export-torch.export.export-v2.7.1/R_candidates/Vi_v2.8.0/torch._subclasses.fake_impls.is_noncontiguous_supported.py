def is_noncontiguous_supported(device):
    return device.type != "hpu"
