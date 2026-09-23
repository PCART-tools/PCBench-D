def _rebuild_tensor(storage, storage_offset, size, stride):
    # first construct a tensor with the correct dtype/device
    t = torch.tensor([], dtype=storage.dtype, device=storage._untyped().device)
    return t.set_(storage._untyped(), storage_offset, size, stride)
