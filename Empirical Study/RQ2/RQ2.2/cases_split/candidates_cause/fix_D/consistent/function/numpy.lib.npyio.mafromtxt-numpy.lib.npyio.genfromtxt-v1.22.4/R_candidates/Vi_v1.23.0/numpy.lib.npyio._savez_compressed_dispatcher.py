def _savez_compressed_dispatcher(file, *args, **kwds):
    yield from args
    yield from kwds.values()
