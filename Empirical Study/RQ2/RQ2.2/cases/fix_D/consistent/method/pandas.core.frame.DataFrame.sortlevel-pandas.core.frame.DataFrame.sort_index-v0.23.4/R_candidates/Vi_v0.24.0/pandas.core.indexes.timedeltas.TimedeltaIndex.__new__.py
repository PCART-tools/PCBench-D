    def __new__(cls, data=None, unit=None, freq=None, start=None, end=None,
                periods=None, closed=None, dtype=_TD_DTYPE, copy=False,
                name=None, verify_integrity=None):

        if verify_integrity is not None:
            warnings.warn("The 'verify_integrity' argument is deprecated, "
                          "will be removed in a future version.",
                          FutureWarning, stacklevel=2)
        else:
            verify_integrity = True

        if data is None:
            freq, freq_infer = dtl.maybe_infer_freq(freq)
            warnings.warn("Creating a TimedeltaIndex by passing range "
                          "endpoints is deprecated.  Use "
                          "`pandas.timedelta_range` instead.",
                          FutureWarning, stacklevel=2)
            result = TimedeltaArray._generate_range(start, end, periods, freq,
                                                    closed=closed)
            return cls._simple_new(result._data, freq=freq, name=name)

        if is_scalar(data):
            raise TypeError('{cls}() must be called with a '
                            'collection of some kind, {data} was passed'
                            .format(cls=cls.__name__, data=repr(data)))

        if isinstance(data, TimedeltaArray):
            if copy:
                data = data.copy()
            return cls._simple_new(data, name=name, freq=freq)

        if (isinstance(data, TimedeltaIndex) and
                freq is None and name is None):
            if copy:
                return data.copy()
            else:
                return data._shallow_copy()

        # - Cases checked above all return/raise before reaching here - #

        tdarr = TimedeltaArray._from_sequence(data, freq=freq, unit=unit,
                                              dtype=dtype, copy=copy)
        return cls._simple_new(tdarr._data, freq=tdarr.freq, name=name)
