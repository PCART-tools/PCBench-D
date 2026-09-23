    def __new__(
        cls, data=None, dtype=None, copy=False, name=None, tupleize_cols=True, **kwargs
    ) -> Index:

        if kwargs:
            warnings.warn(
                "Passing keywords other than 'data', 'dtype', 'copy', 'name', "
                "'tupleize_cols' is deprecated and will raise TypeError in a "
                "future version.  Use the specific Index subclass directly instead.",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )

        from pandas.core.arrays import PandasArray
        from pandas.core.indexes.range import RangeIndex

        name = maybe_extract_name(name, data, cls)

        if dtype is not None:
            dtype = pandas_dtype(dtype)
        if "tz" in kwargs:
            tz = kwargs.pop("tz")
            validate_tz_from_dtype(dtype, tz)
            dtype = tz_to_dtype(tz)

        if type(data) is PandasArray:
            # ensure users don't accidentally put a PandasArray in an index,
            #  but don't unpack StringArray
            data = data.to_numpy()
        if isinstance(dtype, PandasDtype):
            dtype = dtype.numpy_dtype

        data_dtype = getattr(data, "dtype", None)

        # range
        if isinstance(data, (range, RangeIndex)):
            result = RangeIndex(start=data, copy=copy, name=name)
            if dtype is not None:
                return result.astype(dtype, copy=False)
            return result

        elif is_ea_or_datetimelike_dtype(dtype):
            # non-EA dtype indexes have special casting logic, so we punt here
            klass = cls._dtype_to_subclass(dtype)
            if klass is not Index:
                return klass(data, dtype=dtype, copy=copy, name=name, **kwargs)

            ea_cls = dtype.construct_array_type()
            data = ea_cls._from_sequence(data, dtype=dtype, copy=copy)
            disallow_kwargs(kwargs)
            return Index._simple_new(data, name=name)

        elif is_ea_or_datetimelike_dtype(data_dtype):
            data_dtype = cast(DtypeObj, data_dtype)
            klass = cls._dtype_to_subclass(data_dtype)
            if klass is not Index:
                result = klass(data, copy=copy, name=name, **kwargs)
                if dtype is not None:
                    return result.astype(dtype, copy=False)
                return result
            elif dtype is not None:
                # GH#45206
                data = data.astype(dtype, copy=False)

            disallow_kwargs(kwargs)
            data = extract_array(data, extract_numpy=True)
            return Index._simple_new(data, name=name)

        # index-like
        elif (
            isinstance(data, Index)
            and data._is_backward_compat_public_numeric_index
            and dtype is None
        ):
            return data._constructor(data, name=name, copy=copy)
        elif isinstance(data, (np.ndarray, Index, ABCSeries)):

            if isinstance(data, ABCMultiIndex):
                data = data._values

            if dtype is not None:
                # we need to avoid having numpy coerce
                # things that look like ints/floats to ints unless
                # they are actually ints, e.g. '0' and 0.0
                # should not be coerced
                # GH 11836
                data = sanitize_array(data, None, dtype=dtype, copy=copy)

                dtype = data.dtype

            if data.dtype.kind in ["i", "u", "f"]:
                # maybe coerce to a sub-class
                arr = data
            elif data.dtype.kind in ["b", "c"]:
                # No special subclass, and Index._ensure_array won't do this
                #  for us.
                arr = np.asarray(data)
            else:
                arr = com.asarray_tuplesafe(data, dtype=_dtype_obj)

                if dtype is None:
                    arr = _maybe_cast_data_without_dtype(
                        arr, cast_numeric_deprecated=True
                    )
                    dtype = arr.dtype

                    if kwargs:
                        return cls(arr, dtype, copy=copy, name=name, **kwargs)

            klass = cls._dtype_to_subclass(arr.dtype)
            arr = klass._ensure_array(arr, dtype, copy)
            disallow_kwargs(kwargs)
            return klass._simple_new(arr, name)

        elif is_scalar(data):
            raise cls._scalar_data_error(data)
        elif hasattr(data, "__array__"):
            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name, **kwargs)
        else:

            if tupleize_cols and is_list_like(data):
                # GH21470: convert iterable to list before determining if empty
                if is_iterator(data):
                    data = list(data)

                if data and all(isinstance(e, tuple) for e in data):
                    # we must be all tuples, otherwise don't construct
                    # 10697
                    from pandas.core.indexes.multi import MultiIndex

                    return MultiIndex.from_tuples(
                        data, names=name or kwargs.get("names")
                    )
            # other iterable of some kind

            subarr = com.asarray_tuplesafe(data, dtype=_dtype_obj)
            if dtype is None:
                # with e.g. a list [1, 2, 3] casting to numeric is _not_ deprecated
                subarr = _maybe_cast_data_without_dtype(
                    subarr, cast_numeric_deprecated=False
                )
                dtype = subarr.dtype
            return Index(subarr, dtype=dtype, copy=copy, name=name, **kwargs)
