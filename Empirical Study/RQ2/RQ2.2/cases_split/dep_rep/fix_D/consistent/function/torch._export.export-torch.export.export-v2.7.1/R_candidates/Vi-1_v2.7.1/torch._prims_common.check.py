@deprecated(
    "`torch._prims_common.check` is deprecated and will be removed in the future. "
    "Please use `torch._check*` functions instead.",
    category=FutureWarning,
)
def check(
    b: bool, s: Callable[[], str], exc_type: type[Exception] = RuntimeError
) -> None:
    """
    Helper function for raising an error_type (default: RuntimeError) if a boolean condition fails.
    Error message is a callable producing a string (to avoid wasting time
    string formatting in non-error case, and also to make it easier for torchdynamo
    to trace.)

    .. note:: This function is planned for removal in the future. Please use
        `torch._check*` functions instead.
    """
    torch._check_with(exc_type, b, s)
