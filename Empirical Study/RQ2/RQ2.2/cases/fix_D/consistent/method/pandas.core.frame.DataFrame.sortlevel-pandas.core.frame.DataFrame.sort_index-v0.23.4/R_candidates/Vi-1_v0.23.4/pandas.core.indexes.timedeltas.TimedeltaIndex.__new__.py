    def __new__(cls, data=None, unit=None, freq=None, start=None, end=None,
                periods=None, closed=None, dtype=None, copy=False,
                name=None, verify_integrity=True):

        if isinstance(data, TimedeltaIndex) and freq is None and name is None:
            if copy:
                return data.copy()
            else:
                return data._shallow_copy()

        freq_infer = False
        if not isinstance(freq, DateOffset):

            # if a passed freq is None, don't infer automatically
            if freq != 'infer':
                freq = to_offset(freq)
            else:
                freq_infer = True
                freq = None

        if periods is not None:
            if is_float(periods):
                periods = int(periods)
            elif not is_integer(periods):
                msg = 'periods must be a number, got {periods}'
                raise TypeError(msg.format(periods=periods))

        if data is None:
            if freq is None and com._any_none(periods, start, end):
                msg = 'Must provide freq argument if no data is supplied'
                raise ValueError(msg)
            else:
                return cls._generate(start, end, periods, name, freq,
                                     closed=closed)

        if unit is not None:
            data = to_timedelta(data, unit=unit, box=False)

        if not isinstance(data, (np.ndarray, Index, ABCSeries)):
            if is_scalar(data):
                raise ValueError('TimedeltaIndex() must be called with a '
                                 'collection of some kind, %s was passed'
                                 % repr(data))

        # convert if not already
        if getattr(data, 'dtype', None) != _TD_DTYPE:
            data = to_timedelta(data, unit=unit, box=False)
        elif copy:
            data = np.array(data, copy=True)

        # check that we are matching freqs
        if verify_integrity and len(data) > 0:
            if freq is not None and not freq_infer:
                index = cls._simple_new(data, name=name)
                cls._validate_frequency(index, freq)
                index.freq = freq
                return index

        if freq_infer:
            index = cls._simple_new(data, name=name)
            inferred = index.inferred_freq
            if inferred:
                index.freq = to_offset(inferred)
            return index

        return cls._simple_new(data, name=name, freq=freq)
