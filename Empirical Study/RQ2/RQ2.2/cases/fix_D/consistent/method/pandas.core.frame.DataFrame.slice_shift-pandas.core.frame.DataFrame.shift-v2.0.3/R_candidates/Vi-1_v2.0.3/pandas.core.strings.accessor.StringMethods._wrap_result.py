    def _wrap_result(
        self,
        result,
        name=None,
        expand: bool | None = None,
        fill_value=np.nan,
        returns_string: bool = True,
        returns_bool: bool = False,
    ):
        from pandas import (
            Index,
            MultiIndex,
        )

        if not hasattr(result, "ndim") or not hasattr(result, "dtype"):
            if isinstance(result, ABCDataFrame):
                result = result.__finalize__(self._orig, name="str")
            return result
        assert result.ndim < 3

        # We can be wrapping a string / object / categorical result, in which
        # case we'll want to return the same dtype as the input.
        # Or we can be wrapping a numeric output, in which case we don't want
        # to return a StringArray.
        # Ideally the array method returns the right array type.
        if expand is None:
            # infer from ndim if expand is not specified
            expand = result.ndim != 1
        elif expand is True and not isinstance(self._orig, ABCIndex):
            # required when expand=True is explicitly specified
            # not needed when inferred
            if isinstance(result.dtype, ArrowDtype):
                import pyarrow as pa

                from pandas.compat import pa_version_under11p0

                from pandas.core.arrays.arrow.array import ArrowExtensionArray

                value_lengths = result._data.combine_chunks().value_lengths()
                max_len = pa.compute.max(value_lengths).as_py()
                min_len = pa.compute.min(value_lengths).as_py()
                if result._hasna:
                    # ArrowExtensionArray.fillna doesn't work for list scalars
                    result = ArrowExtensionArray(
                        result._data.fill_null([None] * max_len)
                    )
                if min_len < max_len:
                    # append nulls to each scalar list element up to max_len
                    if not pa_version_under11p0:
                        result = ArrowExtensionArray(
                            pa.compute.list_slice(
                                result._data,
                                start=0,
                                stop=max_len,
                                return_fixed_size_list=True,
                            )
                        )
                    else:
                        all_null = np.full(max_len, fill_value=None, dtype=object)
                        values = result.to_numpy()
                        new_values = []
                        for row in values:
                            if len(row) < max_len:
                                nulls = all_null[: max_len - len(row)]
                                row = np.append(row, nulls)
                            new_values.append(row)
                        pa_type = result._data.type
                        result = ArrowExtensionArray(pa.array(new_values, type=pa_type))
                if name is not None:
                    labels = name
                else:
                    labels = range(max_len)
                result = {
                    label: ArrowExtensionArray(pa.array(res))
                    for label, res in zip(labels, (zip(*result.tolist())))
                }
            elif is_object_dtype(result):

                def cons_row(x):
                    if is_list_like(x):
                        return x
                    else:
                        return [x]

                result = [cons_row(x) for x in result]
                if result and not self._is_string:
                    # propagate nan values to match longest sequence (GH 18450)
                    max_len = max(len(x) for x in result)
                    result = [
                        x * max_len if len(x) == 0 or x[0] is np.nan else x
                        for x in result
                    ]

        if not isinstance(expand, bool):
            raise ValueError("expand must be True or False")

        if expand is False:
            # if expand is False, result should have the same name
            # as the original otherwise specified
            if name is None:
                name = getattr(result, "name", None)
            if name is None:
                # do not use logical or, _orig may be a DataFrame
                # which has "name" column
                name = self._orig.name

        # Wait until we are sure result is a Series or Index before
        # checking attributes (GH 12180)
        if isinstance(self._orig, ABCIndex):
            # if result is a boolean np.array, return the np.array
            # instead of wrapping it into a boolean Index (GH 8875)
            if is_bool_dtype(result):
                return result

            if expand:
                result = list(result)
                out = MultiIndex.from_tuples(result, names=name)
                if out.nlevels == 1:
                    # We had all tuples of length-one, which are
                    # better represented as a regular Index.
                    out = out.get_level_values(0)
                return out
            else:
                return Index(result, name=name)
        else:
            index = self._orig.index
            # This is a mess.
            dtype: DtypeObj | str | None
            vdtype = getattr(result, "dtype", None)
            if self._is_string:
                if is_bool_dtype(vdtype):
                    dtype = result.dtype
                elif returns_string:
                    dtype = self._orig.dtype
                else:
                    dtype = vdtype
            else:
                dtype = vdtype

            if expand:
                cons = self._orig._constructor_expanddim
                result = cons(result, columns=name, index=index, dtype=dtype)
            else:
                # Must be a Series
                cons = self._orig._constructor
                result = cons(result, name=name, index=index, dtype=dtype)
            result = result.__finalize__(self._orig, method="str")
            if name is not None and result.ndim == 1:
                # __finalize__ might copy over the original name, but we may
                # want the new name (e.g. str.extract).
                result.name = name
            return result
