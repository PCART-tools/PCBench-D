class DeviceQuantileDMatrix(QuantileDMatrix):
    """ Use `QuantileDMatrix` instead.

    .. deprecated:: 1.7.0

    .. versionadded:: 1.1.0

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        warnings.warn("Please use `QuantileDMatrix` instead.", FutureWarning)
        super().__init__(*args, **kwargs)
