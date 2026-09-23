def reduce_typed_storage_child(storage):
    return (rebuild_typed_storage_child, (storage._storage, type(storage)))
