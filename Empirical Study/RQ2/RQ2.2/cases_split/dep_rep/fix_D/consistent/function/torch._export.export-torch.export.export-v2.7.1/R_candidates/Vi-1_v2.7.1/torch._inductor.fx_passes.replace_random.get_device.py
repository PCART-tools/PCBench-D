def get_device(device):
    if device is not None:
        return device
    return torch.empty([]).device  # default device
