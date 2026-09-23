    def __new__(cls, data=None, dtype=None, copy=False, name=None,
                fastpath=False, tupleize_cols=True, **kwargs):

        if name is None and hasattr(data, 'name'):
            name = data.name

        if fastpath:
            return cls._simple_new(data, name)

        from .range import RangeIndex

        # range
        if isinstance(data, RangeIndex):
            return RangeIndex(start=data, copy=copy, dtype=dtype, name=name)
        elif isinstance(data, range):
            return RangeIndex.from_range(data, copy=copy, dtype=dtype,
                                         name=name)

        # categorical
        if is_categorical_dtype(data) or is_categorical_dtype(dtype):
            from .category import CategoricalIndex
            return CategoricalIndex(data, copy=copy, name=name, **kwargs)

        # interval
        if is_interval_dtype(data):
            from .interval import IntervalIndex
            return IntervalIndex.from_intervals(data, name=name,
                                                copy=copy)

        # index-like
        elif isinstance(data, (np.ndarray, Index, ABCSeries)):

            if (is_datetime64_any_dtype(data) or
                (dtype is not None and is_datetime64_any_dtype(dtype)) or
                    'tz' in kwargs):
                from pandas.core.indexes.datetimes import DatetimeIndex
                result = DatetimeIndex(data, copy=copy, name=name,
                                       dtype=dtype, **kwargs)
                if dtype is not None and is_dtype_equal(_o_dtype, dtype):
                    return Index(result.to_pydatetime(), dtype=_o_dtype)
                else:
                    return result

            elif (is_timedelta64_dtype(data) or
                  (dtype is not None and is_timedelta64_dtype(dtype))):
                from pandas.core.indexes.timedeltas import TimedeltaIndex
                result = TimedeltaIndex(data, copy=copy, name=name, **kwargs)
                if dtype is not None and _o_dtype == dtype:
                    return Index(result.to_pytimedelta(), dtype=_o_dtype)
                else:
                    return result

            if dtype is not None:
                try:

                    # we need to avoid having numpy coerce
                    # things that look like ints/floats to ints unless
                    # they are actually ints, e.g. '0' and 0.0
                    # should not be coerced
                    # GH 11836
                    if is_integer_dtype(dtype):
                        inferred = lib.infer_dtype(data)
                        if inferred == 'integer':
                            data = np.array(data, copy=copy, dtype=dtype)
                        elif inferred in ['floating', 'mixed-integer-float']:
                            if isna(data).any():
                                raise ValueError('cannot convert float '
                                                 'NaN to integer')

                            # If we are actually all equal to integers,
                            # then coerce to integer.
                            try:
                                return cls._try_convert_to_int_index(
                                    data, copy, name)
                            except ValueError:
                                pass

                            # Return an actual float index.
                            from .numeric import Float64Index
                            return Float64Index(data, copy=copy, dtype=dtype,
                                                name=name)

                        elif inferred == 'string':
                            pass
                        else:
                            data = data.astype(dtype)
                    elif is_float_dtype(dtype):
                        inferred = lib.infer_dtype(data)
                        if inferred == 'string':
                            pass
                        else:
                            data = data.astype(dtype)
                    else:
                        data = np.array(data, dtype=dtype, copy=copy)

                except (TypeError, ValueError) as e:
                    msg = str(e)
                    if 'cannot convert float' in msg:
                        raise

            # maybe coerce to a sub-class
            from pandas.core.indexes.period import (
                PeriodIndex, IncompatibleFrequency)
            if isinstance(data, PeriodIndex):
                return PeriodIndex(data, copy=copy, name=name, **kwargs)
            if is_signed_integer_dtype(data.dtype):
                from .numeric import Int64Index
                return Int64Index(data, copy=copy, dtype=dtype, name=name)
            elif is_unsigned_integer_dtype(data.dtype):
                from .numeric import UInt64Index
                return UInt64Index(data, copy=copy, dtype=dtype, name=name)
            elif is_float_dtype(data.dtype):
                from .numeric import Float64Index
                return Float64Index(data, copy=copy, dtype=dtype, name=name)
            elif issubclass(data.dtype.type, np.bool) or is_bool_dtype(data):
                subarr = data.astype('object')
            else:
                subarr = _asarray_tuplesafe(data, dtype=object)

            # _asarray_tuplesafe does not always copy underlying data,
            # so need to make sure that this happens
            if copy:
                subarr = subarr.copy()

            if dtype is None:
                inferred = lib.infer_dtype(subarr)
                if inferred == 'integer':
                    try:
                        return cls._try_convert_to_int_index(
                            subarr, copy, name)
                    except ValueError:
                        pass

                    return Index(subarr, copy=copy,
                                 dtype=object, name=name)
                elif inferred in ['floating', 'mixed-integer-float']:
                    from .numeric import Float64Index
                    return Float64Index(subarr, copy=copy, name=name)
                elif inferred == 'interval':
                    from .interval import IntervalIndex
                    return IntervalIndex.from_intervals(subarr, name=name,
                                                        copy=copy)
                elif inferred == 'boolean':
                    # don't support boolean explicity ATM
                    pass
                elif inferred != 'string':
                    if inferred.startswith('datetime'):
                        if (lib.is_datetime_with_singletz_array(subarr) or
                                'tz' in kwargs):
                            # only when subarr has the same tz
                            from pandas.core.indexes.datetimes import (
                                DatetimeIndex)
                            try:
                                return DatetimeIndex(subarr, copy=copy,
                                                     name=name, **kwargs)
                            except libts.OutOfBoundsDatetime:
                                pass

                    elif inferred.startswith('timedelta'):
                        from pandas.core.indexes.timedeltas import (
                            TimedeltaIndex)
                        return TimedeltaIndex(subarr, copy=copy, name=name,
                                              **kwargs)
                    elif inferred == 'period':
                        try:
                            return PeriodIndex(subarr, name=name, **kwargs)
                        except IncompatibleFrequency:
                            pass
            return cls._simple_new(subarr, name)

        elif hasattr(data, '__array__'):
            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name,
                         **kwargs)
        elif data is None or is_scalar(data):
            cls._scalar_data_error(data)
        else:
            if (tupleize_cols and isinstance(data, list) and data and
                    isinstance(data[0], tuple)):

                # we must be all tuples, otherwise don't construct
                # 10697
                if all(isinstance(e, tuple) for e in data):
                    try:
                        # must be orderable in py3
                        if compat.PY3:
                            sorted(data)
                        from .multi import MultiIndex
                        return MultiIndex.from_tuples(
                            data, names=name or kwargs.get('names'))
                    except (TypeError, KeyError):
                        # python2 - MultiIndex fails on mixed types
                        pass
            # other iterable of some kind
            subarr = _asarray_tuplesafe(data, dtype=object)
            return Index(subarr, dtype=dtype, copy=copy, name=name, **kwargs)
