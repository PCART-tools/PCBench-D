    def __new__(cls, data=None, dtype=None, copy=False, name=None,
                fastpath=None, tupleize_cols=True, **kwargs):

        if name is None and hasattr(data, 'name'):
            name = data.name

        if fastpath is not None:
            warnings.warn("The 'fastpath' keyword is deprecated, and will be "
                          "removed in a future version.",
                          FutureWarning, stacklevel=2)
            if fastpath:
                return cls._simple_new(data, name)

        from .range import RangeIndex
        if isinstance(data, ABCPandasArray):
            # ensure users don't accidentally put a PandasArray in an index.
            data = data.to_numpy()

        # range
        if isinstance(data, RangeIndex):
            return RangeIndex(start=data, copy=copy, dtype=dtype, name=name)
        elif isinstance(data, range):
            return RangeIndex.from_range(data, copy=copy, dtype=dtype,
                                         name=name)

        # categorical
        elif is_categorical_dtype(data) or is_categorical_dtype(dtype):
            from .category import CategoricalIndex
            return CategoricalIndex(data, dtype=dtype, copy=copy, name=name,
                                    **kwargs)

        # interval
        elif ((is_interval_dtype(data) or is_interval_dtype(dtype)) and
              not is_object_dtype(dtype)):
            from .interval import IntervalIndex
            closed = kwargs.get('closed', None)
            return IntervalIndex(data, dtype=dtype, name=name, copy=copy,
                                 closed=closed)

        elif (is_datetime64_any_dtype(data) or
              (dtype is not None and is_datetime64_any_dtype(dtype)) or
                'tz' in kwargs):
            from pandas import DatetimeIndex

            if dtype is not None and is_dtype_equal(_o_dtype, dtype):
                # GH#23524 passing `dtype=object` to DatetimeIndex is invalid,
                #  will raise in the where `data` is already tz-aware.  So
                #  we leave it out of this step and cast to object-dtype after
                #  the DatetimeIndex construction.
                # Note we can pass copy=False because the .astype below
                #  will always make a copy
                result = DatetimeIndex(data, copy=False, name=name, **kwargs)
                return result.astype(object)
            else:
                result = DatetimeIndex(data, copy=copy, name=name,
                                       dtype=dtype, **kwargs)
                return result

        elif (is_timedelta64_dtype(data) or
              (dtype is not None and is_timedelta64_dtype(dtype))):
            from pandas import TimedeltaIndex
            if dtype is not None and is_dtype_equal(_o_dtype, dtype):
                # Note we can pass copy=False because the .astype below
                #  will always make a copy
                result = TimedeltaIndex(data, copy=False, name=name, **kwargs)
                return result.astype(object)
            else:
                result = TimedeltaIndex(data, copy=copy, name=name,
                                        dtype=dtype, **kwargs)
                return result

        elif is_period_dtype(data) and not is_object_dtype(dtype):
            from pandas import PeriodIndex
            result = PeriodIndex(data, copy=copy, name=name, **kwargs)
            return result

        # extension dtype
        elif is_extension_array_dtype(data) or is_extension_array_dtype(dtype):
            data = np.asarray(data)
            if not (dtype is None or is_object_dtype(dtype)):

                # coerce to the provided dtype
                data = dtype.construct_array_type()._from_sequence(
                    data, dtype=dtype, copy=False)

            # coerce to the object dtype
            data = data.astype(object)
            return Index(data, dtype=object, copy=copy, name=name,
                         **kwargs)

        # index-like
        elif isinstance(data, (np.ndarray, Index, ABCSeries)):
            if dtype is not None:
                try:

                    # we need to avoid having numpy coerce
                    # things that look like ints/floats to ints unless
                    # they are actually ints, e.g. '0' and 0.0
                    # should not be coerced
                    # GH 11836
                    if is_integer_dtype(dtype):
                        inferred = lib.infer_dtype(data, skipna=False)
                        if inferred == 'integer':
                            data = maybe_cast_to_integer_array(data, dtype,
                                                               copy=copy)
                        elif inferred in ['floating', 'mixed-integer-float']:
                            if isna(data).any():
                                raise ValueError('cannot convert float '
                                                 'NaN to integer')

                            if inferred == "mixed-integer-float":
                                data = maybe_cast_to_integer_array(data, dtype)

                            # If we are actually all equal to integers,
                            # then coerce to integer.
                            try:
                                return cls._try_convert_to_int_index(
                                    data, copy, name, dtype)
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
                        inferred = lib.infer_dtype(data, skipna=False)
                        if inferred == 'string':
                            pass
                        else:
                            data = data.astype(dtype)
                    else:
                        data = np.array(data, dtype=dtype, copy=copy)

                except (TypeError, ValueError) as e:
                    msg = str(e)
                    if ("cannot convert float" in msg or
                            "Trying to coerce float values to integer" in msg):
                        raise

            # maybe coerce to a sub-class
            from pandas.core.indexes.period import (
                PeriodIndex, IncompatibleFrequency)

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
                subarr = com.asarray_tuplesafe(data, dtype=object)

            # asarray_tuplesafe does not always copy underlying data,
            # so need to make sure that this happens
            if copy:
                subarr = subarr.copy()

            if dtype is None:
                inferred = lib.infer_dtype(subarr, skipna=False)
                if inferred == 'integer':
                    try:
                        return cls._try_convert_to_int_index(
                            subarr, copy, name, dtype)
                    except ValueError:
                        pass

                    return Index(subarr, copy=copy,
                                 dtype=object, name=name)
                elif inferred in ['floating', 'mixed-integer-float']:
                    from .numeric import Float64Index
                    return Float64Index(subarr, copy=copy, name=name)
                elif inferred == 'interval':
                    from .interval import IntervalIndex
                    return IntervalIndex(subarr, name=name, copy=copy)
                elif inferred == 'boolean':
                    # don't support boolean explicitly ATM
                    pass
                elif inferred != 'string':
                    if inferred.startswith('datetime'):
                        if (lib.is_datetime_with_singletz_array(subarr) or
                                'tz' in kwargs):
                            # only when subarr has the same tz
                            from pandas import DatetimeIndex
                            try:
                                return DatetimeIndex(subarr, copy=copy,
                                                     name=name, **kwargs)
                            except tslibs.OutOfBoundsDatetime:
                                pass

                    elif inferred.startswith('timedelta'):
                        from pandas import TimedeltaIndex
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
            if tupleize_cols and is_list_like(data):
                # GH21470: convert iterable to list before determining if empty
                if is_iterator(data):
                    data = list(data)

                if data and all(isinstance(e, tuple) for e in data):
                    # we must be all tuples, otherwise don't construct
                    # 10697
                    from .multi import MultiIndex
                    return MultiIndex.from_tuples(
                        data, names=name or kwargs.get('names'))
            # other iterable of some kind
            subarr = com.asarray_tuplesafe(data, dtype=object)
            return Index(subarr, dtype=dtype, copy=copy, name=name, **kwargs)
