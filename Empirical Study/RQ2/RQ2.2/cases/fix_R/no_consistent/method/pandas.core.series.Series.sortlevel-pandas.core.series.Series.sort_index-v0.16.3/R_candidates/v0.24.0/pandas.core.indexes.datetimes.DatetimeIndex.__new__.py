    def __new__(cls, data=None,
                freq=None, start=None, end=None, periods=None, tz=None,
                normalize=False, closed=None, ambiguous='raise',
                dayfirst=False, yearfirst=False, dtype=None,
                copy=False, name=None, verify_integrity=None):

        if verify_integrity is not None:
            warnings.warn("The 'verify_integrity' argument is deprecated, "
                          "will be removed in a future version.",
                          FutureWarning, stacklevel=2)
        else:
            verify_integrity = True

        if data is None:
            dtarr = DatetimeArray._generate_range(
                start, end, periods,
                freq=freq, tz=tz, normalize=normalize,
                closed=closed, ambiguous=ambiguous)
            warnings.warn("Creating a DatetimeIndex by passing range "
                          "endpoints is deprecated.  Use "
                          "`pandas.date_range` instead.",
                          FutureWarning, stacklevel=2)
            return cls._simple_new(
                dtarr._data, freq=dtarr.freq, tz=dtarr.tz, name=name)

        if is_scalar(data):
            raise TypeError("{cls}() must be called with a "
                            "collection of some kind, {data} was passed"
                            .format(cls=cls.__name__, data=repr(data)))

        # - Cases checked above all return/raise before reaching here - #

        if name is None and hasattr(data, 'name'):
            name = data.name

        dtarr = DatetimeArray._from_sequence(
            data, dtype=dtype, copy=copy, tz=tz, freq=freq,
            dayfirst=dayfirst, yearfirst=yearfirst, ambiguous=ambiguous,
            int_as_wall_time=True)

        subarr = cls._simple_new(dtarr, name=name,
                                 freq=dtarr.freq, tz=dtarr.tz)
        return subarr
