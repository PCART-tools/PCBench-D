    def __new__(cls, data=None, unit=None,
                freq=None, start=None, end=None, periods=None,
                copy=False, name=None,
                closed=None, verify_integrity=True, **kwargs):

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
                raise ValueError('Periods must be a number, got %s' %
                                 str(periods))

        if data is None and freq is None:
            raise ValueError("Must provide freq argument if no data is "
                             "supplied")

        if data is None:
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
                inferred = index.inferred_freq
                if inferred != freq.freqstr:
                    on_freq = cls._generate(
                        index[0], None, len(index), name, freq)
                    if not np.array_equal(index.asi8, on_freq.asi8):
                        raise ValueError('Inferred frequency {0} from passed '
                                         'timedeltas does not conform to '
                                         'passed frequency {1}'
                                         .format(inferred, freq.freqstr))
                index.freq = freq
                return index

        if freq_infer:
            index = cls._simple_new(data, name=name)
            inferred = index.inferred_freq
            if inferred:
                index.freq = to_offset(inferred)
            return index

        return cls._simple_new(data, name=name, freq=freq)
