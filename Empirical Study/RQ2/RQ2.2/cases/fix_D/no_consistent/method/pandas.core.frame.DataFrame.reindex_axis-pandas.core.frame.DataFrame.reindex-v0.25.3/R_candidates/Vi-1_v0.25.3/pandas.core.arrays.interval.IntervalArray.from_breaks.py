    @classmethod
    @Appender(_interval_shared_docs["from_breaks"] % _shared_docs_kwargs)
    def from_breaks(cls, breaks, closed="right", copy=False, dtype=None):
        breaks = maybe_convert_platform_interval(breaks)

        return cls.from_arrays(breaks[:-1], breaks[1:], closed, copy=copy, dtype=dtype)
