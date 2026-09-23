    def _register_loader(idx, size):
        def decorator(func):
            from .TiffTags import TYPES

            if func.__name__.startswith("load_"):
                TYPES[idx] = func.__name__[5:].replace("_", " ")
            _load_dispatch[idx] = size, func  # noqa: F821
            return func

        return decorator
