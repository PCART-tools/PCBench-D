def rebuild_storage_filename(cls, manager, handle, size):
    storage = storage_from_cache(cls, handle)
    if storage is not None:
        return storage._shared_decref()
    storage = cls._new_shared_filename(manager, handle, size)
    shared_cache[handle] = StorageWeakRef(storage)
    return storage._shared_decref()
