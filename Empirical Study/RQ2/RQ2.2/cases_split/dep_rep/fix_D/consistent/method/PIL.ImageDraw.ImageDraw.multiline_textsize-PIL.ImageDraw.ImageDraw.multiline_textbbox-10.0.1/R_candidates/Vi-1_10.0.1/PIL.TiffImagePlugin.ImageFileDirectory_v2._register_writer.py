    def _register_writer(idx):
        def decorator(func):
            _write_dispatch[idx] = func  # noqa: F821
            return func

        return decorator
