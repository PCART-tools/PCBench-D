def map_to_ref(t: Optional[Tensor]) -> Optional[StorageWeakRefWrapper]:
    if not isinstance(t, torch.Tensor):
        assert t is None
        return None
    return StorageWeakRefWrapper(t)
