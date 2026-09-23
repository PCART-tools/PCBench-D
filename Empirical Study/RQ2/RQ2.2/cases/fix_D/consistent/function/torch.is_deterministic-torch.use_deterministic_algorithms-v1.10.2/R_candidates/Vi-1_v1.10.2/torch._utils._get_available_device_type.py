def _get_available_device_type():
    if torch.cuda.is_available():
        return "cuda"
    # add more available device types here
    return None
