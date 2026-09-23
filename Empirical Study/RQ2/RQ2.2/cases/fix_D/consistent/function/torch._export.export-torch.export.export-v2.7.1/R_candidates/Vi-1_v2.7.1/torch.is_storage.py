def is_storage(obj: _Any, /) -> _TypeIs[_Union["TypedStorage", "UntypedStorage"]]:
    r"""Returns True if `obj` is a PyTorch storage object.

    Args:
        obj (Object): Object to test
    """
    return type(obj) in _storage_classes
