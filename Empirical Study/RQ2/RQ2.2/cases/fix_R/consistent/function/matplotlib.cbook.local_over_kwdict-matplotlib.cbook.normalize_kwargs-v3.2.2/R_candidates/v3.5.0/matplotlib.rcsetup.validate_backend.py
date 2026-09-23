def validate_backend(s):
    backend = (
        s if s is _auto_backend_sentinel or s.startswith("module://")
        else _validate_standard_backends(s))
    return backend
