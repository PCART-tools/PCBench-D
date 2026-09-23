def _savez_dispatcher(file, *args, **kwds):
    yield from args
    yield from kwds.values()
