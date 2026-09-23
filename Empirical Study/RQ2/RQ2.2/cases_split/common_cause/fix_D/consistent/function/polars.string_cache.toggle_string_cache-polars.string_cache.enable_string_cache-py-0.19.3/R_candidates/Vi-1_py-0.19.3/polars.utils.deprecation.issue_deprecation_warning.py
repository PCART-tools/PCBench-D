def issue_deprecation_warning(message: str, *, version: str) -> None:
    """
    Issue a deprecation warning.

    Parameters
    ----------
    message
        The message associated with the warning.
    version
        The Polars version number in which the warning is first issued.
        This argument is used to help developers determine when to remove the
        deprecated functionality.

    """
    warnings.warn(message, DeprecationWarning, stacklevel=find_stacklevel())
