def _parse_inputs(
    actual: Any, expected: Any, *, allow_subclasses: bool
) -> Tuple[Optional[_TestingErrorMeta], Optional[Union[_TensorPair, List, Dict]]]:
    """Parses the positional inputs by constructing :class:`_TensorPair`'s from corresponding tensor-or-scalar-likes.


    :class:`~collections.abc.Sequence`'s or :class:`~collections.abc.Mapping`'s are parsed elementwise. Parsing is
    performed recursively and thus nested containers are supported. The hierarchy of the containers is preserved, but
    sequences are returned as :class:`list` and mappings as :class:`dict`.

    Args:
        actual (Any): Actual input.
        expected (Any): Expected input.
        allow_subclasses (bool): If ``True`` (default) and except for Python scalars, inputs of directly related types
            are allowed. Otherwise type equality is required.

    Returns:
        (Tuple[Optional[_TestingErrorMeta], Optional[Union[_TensorPair, List, Dict]]]): The two elements are
            orthogonal, i.e. if the first is ``None`` the second will be valid and vice versa. Returns
            :class:`_TestingErrorMeta` if the length of two sequences or the keys of two mappings do not match.
            Additionally, returns any error meta from :func:`_to_tensor_pair`.

    """
    error_meta: Optional[_TestingErrorMeta]

    # We explicitly exclude str's here since they are self-referential and would cause an infinite recursion loop:
    # "a" == "a"[0][0]...
    if (
        isinstance(actual, collections.abc.Sequence)
        and not isinstance(actual, str)
        and isinstance(expected, collections.abc.Sequence)
        and not isinstance(expected, str)
    ):
        actual_len = len(actual)
        expected_len = len(expected)
        if actual_len != expected_len:
            error_meta = _TestingErrorMeta(
                AssertionError, f"The length of the sequences mismatch: {actual_len} != {expected_len}"
            )
            return error_meta, None

        pair_list = []
        for idx in range(actual_len):
            error_meta, pair = _parse_inputs(actual[idx], expected[idx], allow_subclasses=allow_subclasses)
            if error_meta:
                error_meta = error_meta.amend_msg(postfix=f"\n\n{_SEQUENCE_MSG_FMTSTR.format(idx)}")
                return error_meta, None

            pair_list.append(pair)
        else:
            return None, pair_list

    elif isinstance(actual, collections.abc.Mapping) and isinstance(expected, collections.abc.Mapping):
        actual_keys = set(actual.keys())
        expected_keys = set(expected.keys())
        if actual_keys != expected_keys:
            missing_keys = expected_keys - actual_keys
            additional_keys = actual_keys - expected_keys
            error_meta = _TestingErrorMeta(
                AssertionError,
                f"The keys of the mappings do not match:\n"
                f"Missing keys in the actual mapping: {sorted(missing_keys)}\n"
                f"Additional keys in the actual mapping: {sorted(additional_keys)}",
            )
            return error_meta, None

        pair_dict = {}
        for key in sorted(actual_keys):
            error_meta, pair = _parse_inputs(actual[key], expected[key], allow_subclasses=allow_subclasses)
            if error_meta:
                error_meta = error_meta.amend_msg(postfix=f"\n\n{_MAPPING_MSG_FMTSTR.format(key)}")
                return error_meta, None

            pair_dict[key] = pair
        else:
            return None, pair_dict

    else:
        return _to_tensor_pair(actual, expected, allow_subclasses=allow_subclasses)
