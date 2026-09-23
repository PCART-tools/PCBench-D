def _load_from_bytes(b):
    return torch.load(io.BytesIO(b))
