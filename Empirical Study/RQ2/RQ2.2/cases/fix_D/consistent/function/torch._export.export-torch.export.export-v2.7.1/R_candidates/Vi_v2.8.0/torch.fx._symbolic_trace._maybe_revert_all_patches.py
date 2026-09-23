@contextlib.contextmanager
def _maybe_revert_all_patches():
    current_patcher = CURRENT_PATCHER
    patches_made = None
    patches_removed = None
    try:
        if current_patcher is not None:
            patches_removed = current_patcher.revert_all_patches()
        yield
    finally:
        if current_patcher is not None:
            patches_made = current_patcher.reapply_all_patches()
        assert patches_made == patches_removed, (
            "CURRENT_PATCHER was changed during a revert_all_patches"
        )
