def _recursive_subclasses(cls):
    yield cls
    for subcls in cls.__subclasses__():
        yield from _recursive_subclasses(subcls)
