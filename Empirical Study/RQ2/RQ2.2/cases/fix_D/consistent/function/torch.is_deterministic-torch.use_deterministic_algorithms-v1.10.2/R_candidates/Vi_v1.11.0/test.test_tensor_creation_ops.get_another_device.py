def get_another_device(device):
    return "cuda" if torch.device(device).type == "cpu" else "cpu"
