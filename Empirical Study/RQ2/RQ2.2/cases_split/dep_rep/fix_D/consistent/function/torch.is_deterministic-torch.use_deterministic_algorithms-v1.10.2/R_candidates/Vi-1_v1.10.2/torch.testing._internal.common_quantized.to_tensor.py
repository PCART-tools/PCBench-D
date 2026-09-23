def to_tensor(X, device):
    return torch.tensor(X).to(device=torch.device(device), dtype=torch.float32)
