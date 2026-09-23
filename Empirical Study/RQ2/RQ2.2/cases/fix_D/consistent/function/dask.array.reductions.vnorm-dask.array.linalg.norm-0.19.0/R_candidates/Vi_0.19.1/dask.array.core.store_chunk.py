def store_chunk(x, out, index, lock, return_stored):
    return load_store_chunk(x, out, index, lock, return_stored, False)
