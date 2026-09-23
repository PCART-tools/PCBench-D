    @deprecate_kwarg(old_arg_name='infer_dst', new_arg_name='ambiguous',
                     mapping={True: 'infer', False: 'raise'})
    def __new__(cls, data=None,
                freq=None, start=None, end=None, periods=None,
                copy=False, name=None, tz=None,
                verify_integrity=True, normalize=False,
                closed=None, ambiguous='raise', dtype=None, **kwargs):

        # This allows to later ensure that the 'copy' parameter is honored:
        if isinstance(data, Index):
            ref_to_data = data._data
        else:
            ref_to_data = data

        if name is None and hasattr(data, 'name'):
            name = data.name

        dayfirst = kwargs.pop('dayfirst', None)
        yearfirst = kwargs.pop('yearfirst', None)

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

        # if dtype has an embeded tz, capture it
        if dtype is not None:
            try:
                dtype = DatetimeTZDtype.construct_from_string(dtype)
                dtz = getattr(dtype, 'tz', None)
                if dtz is not None:
                    if tz is not None and str(tz) != str(dtz):
                        raise ValueError("cannot supply both a tz and a dtype"
                                         " with a tz")
                    tz = dtz
            except TypeError:
                pass

        if data is None:
            return cls._generate(start, end, periods, name, freq,
                                 tz=tz, normalize=normalize, closed=closed,
                                 ambiguous=ambiguous)

        if not isinstance(data, (np.ndarray, Index, ABCSeries)):
            if is_scalar(data):
                raise ValueError('DatetimeIndex() must be called with a '
                                 'collection of some kind, %s was passed'
                                 % repr(data))
            # other iterable of some kind
            if not isinstance(data, (list, tuple)):
                data = list(data)
            data = np.asarray(data, dtype='O')
        elif isinstance(data, ABCSeries):
            data = data._values

        # data must be Index or np.ndarray here
        if not (is_datetime64_dtype(data) or is_datetimetz(data) or
                is_integer_dtype(data)):
            data = tools.to_datetime(data, dayfirst=dayfirst,
                                     yearfirst=yearfirst)

        if issubclass(data.dtype.type, np.datetime64) or is_datetimetz(data):

            if isinstance(data, DatetimeIndex):
                if tz is None:
                    tz = data.tz
                elif data.tz is None:
                    data = data.tz_localize(tz, ambiguous=ambiguous)
                else:
                    # the tz's must match
                    if str(tz) != str(data.tz):
                        msg = ('data is already tz-aware {0}, unable to '
                               'set specified tz: {1}')
                        raise TypeError(msg.format(data.tz, tz))

                subarr = data.values

                if freq is None:
                    freq = data.offset
                    verify_integrity = False
            else:
                if data.dtype != _NS_DTYPE:
                    subarr = libts.cast_to_nanoseconds(data)
                else:
                    subarr = data
        else:
            # must be integer dtype otherwise
            if isinstance(data, Int64Index):
                raise TypeError('cannot convert Int64Index->DatetimeIndex')
            if data.dtype != _INT64_DTYPE:
                data = data.astype(np.int64)
            subarr = data.view(_NS_DTYPE)

        if isinstance(subarr, DatetimeIndex):
            if tz is None:
                tz = subarr.tz
        else:
            if tz is not None:
                tz = libts.maybe_get_tz(tz)

                if (not isinstance(data, DatetimeIndex) or
                        getattr(data, 'tz', None) is None):
                    # Convert tz-naive to UTC
                    ints = subarr.view('i8')
                    subarr = libts.tz_localize_to_utc(ints, tz,
                                                      ambiguous=ambiguous)
                subarr = subarr.view(_NS_DTYPE)

        subarr = cls._simple_new(subarr, name=name, freq=freq, tz=tz)
        if dtype is not None:
            if not is_dtype_equal(subarr.dtype, dtype):
                # dtype must be coerced to DatetimeTZDtype above
                if subarr.tz is not None:
                    raise ValueError("cannot localize from non-UTC data")

        if verify_integrity and len(subarr) > 0:
            if freq is not None and not freq_infer:
                inferred = subarr.inferred_freq
                if inferred != freq.freqstr:
                    on_freq = cls._generate(subarr[0], None, len(subarr), None,
                                            freq, tz=tz, ambiguous=ambiguous)
                    if not np.array_equal(subarr.asi8, on_freq.asi8):
                        raise ValueError('Inferred frequency {0} from passed '
                                         'dates does not conform to passed '
                                         'frequency {1}'
                                         .format(inferred, freq.freqstr))

        if freq_infer:
            inferred = subarr.inferred_freq
            if inferred:
                subarr.offset = to_offset(inferred)

        return subarr._deepcopy_if_needed(ref_to_data, copy)
