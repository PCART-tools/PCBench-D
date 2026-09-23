class PoolLimits(Limits):
    def __init__(self, **kwargs: typing.Any) -> None:
        warn_deprecated(
            "httpx.PoolLimits(...) is deprecated and will raise errors in the future. "
            "Use httpx.Limits(...) instead."
        )
        super().__init__(**kwargs)
