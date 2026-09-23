@contextlib.contextmanager
def _new_patcher():
    global CURRENT_PATCHER
    prior_patcher = CURRENT_PATCHER
    try:
        CURRENT_PATCHER = _Patcher()
        yield CURRENT_PATCHER
    finally:
        # Clear all the patches made by when using current patcher.
        assert CURRENT_PATCHER is not None
        CURRENT_PATCHER.revert_all_patches()
        CURRENT_PATCHER = prior_patcher
