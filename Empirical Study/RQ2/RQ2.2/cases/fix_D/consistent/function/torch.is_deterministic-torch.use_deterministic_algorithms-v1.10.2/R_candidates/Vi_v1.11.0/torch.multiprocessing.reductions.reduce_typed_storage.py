def reduce_typed_storage(storage):
    return (rebuild_typed_storage, (storage._storage, storage.dtype))
