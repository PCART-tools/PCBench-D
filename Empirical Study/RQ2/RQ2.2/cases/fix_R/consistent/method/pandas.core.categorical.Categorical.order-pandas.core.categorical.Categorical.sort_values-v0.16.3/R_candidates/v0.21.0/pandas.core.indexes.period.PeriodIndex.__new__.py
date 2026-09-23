    def __new__(cls, data=None, ordinal=None, freq=None, start=None, end=None,
                periods=None, copy=False, name=None, tz=None, dtype=None,
                **kwargs):

        if periods is not None:
            if is_float(periods):
                periods = int(periods)
            elif not is_integer(periods):
                msg = 'periods must be a number, got {periods}'
                raise TypeError(msg.format(periods=periods))

        if name is None and hasattr(data, 'name'):
            name = data.name

        if dtype is not None:
            dtype = pandas_dtype(dtype)
            if not is_period_dtype(dtype):
                raise ValueError('dtype must be PeriodDtype')
            if freq is None:
                freq = dtype.freq
            elif freq != dtype.freq:
                msg = 'specified freq and dtype are different'
                raise IncompatibleFrequency(msg)

        # coerce freq to freq object, otherwise it can be coerced elementwise
        # which is slow
        if freq:
            freq = Period._maybe_convert_freq(freq)

        if data is None:
            if ordinal is not None:
                data = np.asarray(ordinal, dtype=np.int64)
            else:
                data, freq = cls._generate_range(start, end, periods,
                                                 freq, kwargs)
            return cls._from_ordinals(data, name=name, freq=freq)

        if isinstance(data, PeriodIndex):
            if freq is None or freq == data.freq:  # no freq change
                freq = data.freq
                data = data._values
            else:
                base1, _ = _gfc(data.freq)
                base2, _ = _gfc(freq)
                data = period.period_asfreq_arr(data._values,
                                                base1, base2, 1)
            return cls._simple_new(data, name=name, freq=freq)

        # not array / index
        if not isinstance(data, (np.ndarray, PeriodIndex,
                                 DatetimeIndex, Int64Index)):
            if is_scalar(data) or isinstance(data, Period):
                cls._scalar_data_error(data)

            # other iterable of some kind
            if not isinstance(data, (list, tuple)):
                data = list(data)

            data = np.asarray(data)

        # datetime other than period
        if is_datetime64_dtype(data.dtype):
            data = dt64arr_to_periodarr(data, freq, tz)
            return cls._from_ordinals(data, name=name, freq=freq)

        # check not floats
        if infer_dtype(data) == 'floating' and len(data) > 0:
            raise TypeError("PeriodIndex does not allow "
                            "floating point in construction")

        # anything else, likely an array of strings or periods
        data = _ensure_object(data)
        freq = freq or period.extract_freq(data)
        data = period.extract_ordinals(data, freq)
        return cls._from_ordinals(data, name=name, freq=freq)
