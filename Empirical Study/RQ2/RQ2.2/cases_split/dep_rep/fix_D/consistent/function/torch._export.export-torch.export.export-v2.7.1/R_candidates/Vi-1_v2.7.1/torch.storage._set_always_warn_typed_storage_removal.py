def _set_always_warn_typed_storage_removal(always_warn):
    global _always_warn_typed_storage_removal
    assert isinstance(always_warn, bool)
    _always_warn_typed_storage_removal = always_warn
