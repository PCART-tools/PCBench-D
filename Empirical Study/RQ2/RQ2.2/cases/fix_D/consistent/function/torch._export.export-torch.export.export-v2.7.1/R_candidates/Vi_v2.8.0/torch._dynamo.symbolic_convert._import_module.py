@functools.cache
def _import_module(name: str) -> types.ModuleType:
    """
    Import the named module and cache the result. importlib.import_module()
    seems to do some filesystem checking to validate the name so not caching
    this can be slow.
    """
    return importlib.import_module(name)
