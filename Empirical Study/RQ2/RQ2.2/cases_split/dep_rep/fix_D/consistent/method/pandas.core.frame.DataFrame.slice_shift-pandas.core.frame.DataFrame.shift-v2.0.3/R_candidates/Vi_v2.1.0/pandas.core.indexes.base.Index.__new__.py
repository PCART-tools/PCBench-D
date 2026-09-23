    def __new__(
        cls,
        data=None,
        dtype=None,
        copy: bool = False,
        name=None,
        tupleize_cols: bool = True,
    ) -> Index:
        from pandas.core.indexes.range import RangeIndex

        name = maybe_extract_name(name, data, cls)

        if dtype is not None:
            dtype = pandas_dtype(dtype)

        data_dtype = getattr(data, "dtype", None)

        refs = None
        if not copy and isinstance(data, (ABCSeries, Index)):
            refs = data._references

        # range
        if isinstance(data, (range, RangeIndex)):
            result = RangeIndex(start=data, copy=copy, name=name)
            if dtype is not None:
                return result.astype(dtype, copy=False)
            return result

        elif is_ea_or_datetimelike_dtype(dtype):
            # non-EA dtype indexes have special casting logic, so we punt here
            pass

        elif is_ea_or_datetimelike_dtype(data_dtype):
            pass

        elif isinstance(data, (np.ndarray, Index, ABCSeries)):
            if isinstance(data, ABCMultiIndex):
                data = data._values

            if data.dtype.kind not in "iufcbmM":
                # GH#11836 we need to avoid having numpy coerce
                # things that look like ints/floats to ints unless
                # they are actually ints, e.g. '0' and 0.0
                # should not be coerced
                data = com.asarray_tuplesafe(data, dtype=_dtype_obj)

        elif is_scalar(data):
            raise cls._raise_scalar_data_error(data)
        elif hasattr(data, "__array__"):
            return Index(np.asarray(data), dtype=dtype, copy=copy, name=name)
        elif not is_list_like(data) and not isinstance(data, memoryview):
            # 2022-11-16 the memoryview check is only necessary on some CI
            #  builds, not clear why
            raise cls._raise_scalar_data_error(data)

        else:
            if tupleize_cols:
                # GH21470: convert iterable to list before determining if empty
                if is_iterator(data):
                    data = list(data)

                if data and all(isinstance(e, tuple) for e in data):
                    # we must be all tuples, otherwise don't construct
                    # 10697
                    from pandas.core.indexes.multi import MultiIndex

                    return MultiIndex.from_tuples(data, names=name)
            # other iterable of some kind

            if not isinstance(data, (list, tuple)):
                # we allow set/frozenset, which Series/sanitize_array does not, so
                #  cast to list here
                data = list(data)
            if len(data) == 0:
                # unlike Series, we default to object dtype:
                data = np.array(data, dtype=object)

            if len(data) and isinstance(data[0], tuple):
                # Ensure we get 1-D array of tuples instead of 2D array.
                data = com.asarray_tuplesafe(data, dtype=_dtype_obj)

        try:
            arr = sanitize_array(data, None, dtype=dtype, copy=copy)
        except ValueError as err:
            if "index must be specified when data is not list-like" in str(err):
                raise cls._raise_scalar_data_error(data) from err
            if "Data must be 1-dimensional" in str(err):
                raise ValueError("Index data must be 1-dimensional") from err
            raise
        arr = ensure_wrapped_if_datetimelike(arr)

        klass = cls._dtype_to_subclass(arr.dtype)

        arr = klass._ensure_array(arr, arr.dtype, copy=False)
        return klass._simple_new(arr, name, refs=refs)
