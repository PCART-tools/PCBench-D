    @classmethod
    @Appender(_interval_shared_docs["from_arrays"] % _shared_docs_kwargs)
    def from_arrays(cls, left, right, closed="right", copy=False, dtype=None):
        left = maybe_convert_platform_interval(left)
        right = maybe_convert_platform_interval(right)

        return cls._simple_new(
            left, right, closed, copy=copy, dtype=dtype, verify_integrity=True
        )
