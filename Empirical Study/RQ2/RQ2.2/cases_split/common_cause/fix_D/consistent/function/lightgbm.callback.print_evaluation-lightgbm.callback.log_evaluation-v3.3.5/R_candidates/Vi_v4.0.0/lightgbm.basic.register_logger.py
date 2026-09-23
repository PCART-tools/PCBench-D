def register_logger(
    logger: Any, info_method_name: str = "info", warning_method_name: str = "warning"
) -> None:
    """Register custom logger.

    Parameters
    ----------
    logger : Any
        Custom logger.
    info_method_name : str, optional (default="info")
        Method used to log info messages.
    warning_method_name : str, optional (default="warning")
        Method used to log warning messages.
    """
    if not _has_method(logger, info_method_name) or not _has_method(logger, warning_method_name):
        raise TypeError(
            f"Logger must provide '{info_method_name}' and '{warning_method_name}' method"
        )

    global _LOGGER, _INFO_METHOD_NAME, _WARNING_METHOD_NAME
    _LOGGER = logger
    _INFO_METHOD_NAME = info_method_name
    _WARNING_METHOD_NAME = warning_method_name
