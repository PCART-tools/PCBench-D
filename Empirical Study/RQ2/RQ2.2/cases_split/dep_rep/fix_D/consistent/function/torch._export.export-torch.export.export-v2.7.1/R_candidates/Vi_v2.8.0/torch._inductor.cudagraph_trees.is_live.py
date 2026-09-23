def is_live(weak_ref: Optional[StorageWeakRefWrapper]) -> bool:
    return maybe_deref(weak_ref) is not None
