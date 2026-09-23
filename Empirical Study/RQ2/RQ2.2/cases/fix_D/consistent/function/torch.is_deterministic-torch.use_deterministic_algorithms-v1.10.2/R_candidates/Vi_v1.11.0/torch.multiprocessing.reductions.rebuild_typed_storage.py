def rebuild_typed_storage(storage, dtype):
    return torch.storage._TypedStorage(wrap_storage=storage, dtype=dtype)
