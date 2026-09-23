def _check_types(actual: Any, expected: Any, *, allow_subclasses: bool) -> Optional[_TestingErrorMeta]:
    # We exclude numbers here, since numbers of different type, e.g. int vs. float, should be treated the same as
    # tensors with different dtypes. Without user input, passing numbers of different types will still fail, but this
    # can be disabled by setting `check_dtype=False`.
    if isinstance(actual, numbers.Number) and isinstance(expected, numbers.Number):
        return None

    msg_fmtstr = f"Except for Python scalars, {{}}, but got {type(actual)} and {type(expected)} instead."
    directly_related = isinstance(actual, type(expected)) or isinstance(expected, type(actual))
    if not directly_related:
        return _TestingErrorMeta(AssertionError, msg_fmtstr.format("input types need to be directly related"))

    if allow_subclasses or type(actual) is type(expected):
        return None

    return _TestingErrorMeta(AssertionError, msg_fmtstr.format("type equality is required if allow_subclasses=False"))
