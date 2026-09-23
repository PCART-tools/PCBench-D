def _get_device_attr(get_member):
    device_type = _get_available_device_type()
    if device_type and device_type.lower() == "cuda":
        return get_member(torch.cuda)
    # add more available device types here
    return None
