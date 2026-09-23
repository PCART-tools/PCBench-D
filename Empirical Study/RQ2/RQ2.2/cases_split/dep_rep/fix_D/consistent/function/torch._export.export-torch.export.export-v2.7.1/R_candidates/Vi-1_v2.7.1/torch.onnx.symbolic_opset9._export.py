def _export(name: str):
    """Exports the function in the current global namespace."""

    def wrapper(func):
        globals()[name] = func
        __all__.append(name)
        return func

    return wrapper
