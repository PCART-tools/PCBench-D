    def __new__(cls, data=None, dtype=None, copy=False, name=None, fastpath=False,
                tupleize_cols=True, **kwargs):

        # no class inference!
        if fastpath:
            return cls._simple_new(data, name)

        from pandas.tseries.period import PeriodIndex
        if isinstance(data, (np.ndarray, Index, ABCSeries)):
            if issubclass(data.dtype.type, np.datetime64):
                from pandas.tseries.index import DatetimeIndex
                result = DatetimeIndex(data, copy=copy, name=name, **kwargs)
                if dtype is not None and _o_dtype == dtype:
                    return Index(result.to_pydatetime(), dtype=_o_dtype)
                else:
                    return result
            elif issubclass(data.dtype.type, np.timedelta64):
                from pandas.tseries.tdi import TimedeltaIndex
                result = TimedeltaIndex(data, copy=copy, name=name, **kwargs)
                if dtype is not None and _o_dtype == dtype:
                    return Index(result.to_pytimedelta(), dtype=_o_dtype)
                else:
                    return result

            if dtype is not None:
                try:
                    data = np.array(data, dtype=dtype, copy=copy)
                except TypeError:
                    pass

            # maybe coerce to a sub-class
            if isinstance(data, PeriodIndex):
                return PeriodIndex(data, copy=copy, name=name, **kwargs)
            if issubclass(data.dtype.type, np.integer):
                return Int64Index(data, copy=copy, dtype=dtype, name=name)
            elif issubclass(data.dtype.type, np.floating):
                return Float64Index(data, copy=copy, dtype=dtype, name=name)
            elif issubclass(data.dtype.type, np.bool) or is_bool_dtype(data):
                subarr = data.astype('object')
            else:
                subarr = com._asarray_tuplesafe(data, dtype=object)

            # _asarray_tuplesafe does not always copy underlying data,
            # so need to make sure that this happens
            if copy:
                subarr = subarr.copy()

        elif hasattr(data, '__array__'):
            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name,
                         **kwargs)
        elif data is None or np.isscalar(data):
            cls._scalar_data_error(data)
        else:
            if tupleize_cols and isinstance(data, list) and data:
                try:
                    sorted(data)
                    has_mixed_types = False
                except (TypeError, UnicodeDecodeError):
                    has_mixed_types = True  # python3 only
                if isinstance(data[0], tuple) and not has_mixed_types:
                    try:
                        return MultiIndex.from_tuples(
                            data, names=name or kwargs.get('names'))
                    except (TypeError, KeyError):
                        pass  # python2 - MultiIndex fails on mixed types
            # other iterable of some kind
            subarr = com._asarray_tuplesafe(data, dtype=object)

        if dtype is None:
            inferred = lib.infer_dtype(subarr)
            if inferred == 'integer':
                return Int64Index(subarr.astype('i8'), copy=copy, name=name)
            elif inferred in ['floating', 'mixed-integer-float']:
                return Float64Index(subarr, copy=copy, name=name)
            elif inferred == 'boolean':
                # don't support boolean explicity ATM
                pass
            elif inferred != 'string':
                if (inferred.startswith('datetime') or
                        tslib.is_timestamp_array(subarr)):
                    from pandas.tseries.index import DatetimeIndex
                    return DatetimeIndex(subarr, copy=copy, name=name, **kwargs)
                elif (inferred.startswith('timedelta') or
                        lib.is_timedelta_array(subarr)):
                    from pandas.tseries.tdi import TimedeltaIndex
                    return TimedeltaIndex(subarr, copy=copy, name=name, **kwargs)
                elif inferred == 'period':
                    return PeriodIndex(subarr, name=name, **kwargs)

        return cls._simple_new(subarr, name)
