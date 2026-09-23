@contextlib.contextmanager
def disable_cache_limit():
    prior = config.recompile_limit
    config.recompile_limit = sys.maxsize
    prior_acc_limit = config.accumulated_recompile_limit
    config.accumulated_recompile_limit = sys.maxsize

    try:
        yield
    finally:
        config.recompile_limit = prior
        config.accumulated_recompile_limit = prior_acc_limit
