def _rebuild_tensor(storage, storage_offset, size, stride):
    # first construct a tensor with the correct dtype/device
    t = torch.tensor([], dtype=storage.dtype, device=storage.device)
    return t.set_(storage, storage_offset, size, stride)
