def _check_pair_close(
    pair: Union[_TensorPair, List, Dict],
    **kwargs: Any,
) -> Optional[_TestingErrorMeta]:
    """Checks input pairs.

    :class:`list`'s or :class:`dict`'s are checked elementwise. Checking is performed recursively and thus nested
    containers are supported.

    Args:
        pair (Union[_TensorPair, List, Dict]): Input pair.
        **kwargs (Any): Keyword arguments passed to :func:`__check_tensors_close`.

    Returns:
        (Optional[_TestingErrorMeta]): Return value of :attr:`check_tensors`.
    """
    if isinstance(pair, list):
        for idx, pair_item in enumerate(pair):
            error_meta = _check_pair_close(pair_item, **kwargs)
            if error_meta:
                return error_meta.amend_msg(postfix=f"\n\n{_SEQUENCE_MSG_FMTSTR.format(idx)}")
        else:
            return None
    elif isinstance(pair, dict):
        for key, pair_item in pair.items():
            error_meta = _check_pair_close(pair_item, **kwargs)
            if error_meta:
                return error_meta.amend_msg(postfix=f"\n\n{_MAPPING_MSG_FMTSTR.format(key)}")
        else:
            return None
    else:  # isinstance(pair, TensorPair)
        return _check_tensors_close(pair.actual, pair.expected, **kwargs)
