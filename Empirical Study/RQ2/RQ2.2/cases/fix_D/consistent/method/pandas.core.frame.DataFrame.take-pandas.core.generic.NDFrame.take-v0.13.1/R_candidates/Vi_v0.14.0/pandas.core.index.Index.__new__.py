    def __new__(cls, data, dtype=None, copy=False, name=None, fastpath=False,
                tupleize_cols=True, **kwargs):

        # no class inference!
        if fastpath:
            return cls._simple_new(data, name)

        from pandas.tseries.period import PeriodIndex
        if isinstance(data, (np.ndarray, ABCSeries)):
            if issubclass(data.dtype.type, np.datetime64):
                from pandas.tseries.index import DatetimeIndex
                result = DatetimeIndex(data, copy=copy, name=name, **kwargs)
                if dtype is not None and _o_dtype == dtype:
                    return Index(result.to_pydatetime(), dtype=_o_dtype)
                else:
                    return result
            elif issubclass(data.dtype.type, np.timedelta64):
                return Int64Index(data, copy=copy, name=name)

            if dtype is not None:
                try:
                    data = np.array(data, dtype=dtype, copy=copy)
                except TypeError:
                    pass
            elif isinstance(data, PeriodIndex):
                return PeriodIndex(data, copy=copy, name=name, **kwargs)

            if issubclass(data.dtype.type, np.integer):
                return Int64Index(data, copy=copy, dtype=dtype, name=name)

            subarr = com._asarray_tuplesafe(data, dtype=object)

            # _asarray_tuplesafe does not always copy underlying data,
            # so need to make sure that this happens
            if copy:
                subarr = subarr.copy()

        elif np.isscalar(data):
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
            elif inferred != 'string':
                if (inferred.startswith('datetime') or
                        tslib.is_timestamp_array(subarr)):
                    from pandas.tseries.index import DatetimeIndex
                    return DatetimeIndex(subarr, copy=copy, name=name, **kwargs)
                elif inferred == 'period':
                    return PeriodIndex(subarr, name=name, **kwargs)

        subarr = subarr.view(cls)
        # could also have a _set_name, but I don't think it's really necessary
        subarr._set_names([name])
        return subarr
