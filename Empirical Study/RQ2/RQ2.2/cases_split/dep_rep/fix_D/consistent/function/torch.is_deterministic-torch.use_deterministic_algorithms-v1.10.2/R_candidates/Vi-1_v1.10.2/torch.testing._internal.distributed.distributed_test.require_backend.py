def require_backend(backends):
    if BACKEND not in backends:
        return sandcastle_skip("Test requires backend to be one of %s" % backends)
    return lambda func: func
