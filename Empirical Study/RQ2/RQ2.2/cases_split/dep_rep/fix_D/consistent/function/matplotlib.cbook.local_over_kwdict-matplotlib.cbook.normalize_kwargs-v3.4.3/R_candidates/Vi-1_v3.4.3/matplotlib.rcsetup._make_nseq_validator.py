@_api.deprecated("3.3")
def _make_nseq_validator(cls, n=None, allow_none=False):

    def validator(s):
        """Convert *n* objects using ``cls``, or raise."""
        if isinstance(s, str):
            s = [x.strip() for x in s.split(',')]
            if n is not None and len(s) != n:
                raise ValueError(
                    f'Expected exactly {n} comma-separated values, '
                    f'but got {len(s)} comma-separated values: {s}')
        else:
            if n is not None and len(s) != n:
                raise ValueError(
                    f'Expected exactly {n} values, '
                    f'but got {len(s)} values: {s}')
        try:
            return [cls(val) if not allow_none or val is not None else val
                    for val in s]
        except ValueError as e:
            raise ValueError(
                f'Could not convert all entries to {cls.__name__}s') from e

    return validator
