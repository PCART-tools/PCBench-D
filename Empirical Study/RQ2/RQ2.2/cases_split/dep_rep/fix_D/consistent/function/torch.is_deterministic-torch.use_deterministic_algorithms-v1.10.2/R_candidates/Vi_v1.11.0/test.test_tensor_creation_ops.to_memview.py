def to_memview(tensor):
    return memoryview(to_numpy(tensor))
