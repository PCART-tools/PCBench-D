    def _agg_py_fallback(
        self, values: ArrayLike, ndim: int, alt: Callable
    ) -> ArrayLike:
        """
        Fallback to pure-python aggregation if _cython_operation raises
        NotImplementedError.
        """
        # We get here with a) EADtypes and b) object dtype

        if values.ndim == 1:
            # For DataFrameGroupBy we only get here with ExtensionArray
            ser = Series(values)
        else:
            # We only get here with values.dtype == object
            # TODO: special case not needed with ArrayManager
            df = DataFrame(values.T)
            # bc we split object blocks in grouped_reduce, we have only 1 col
            # otherwise we'd have to worry about block-splitting GH#39329
            assert df.shape[1] == 1
            # Avoid call to self.values that can occur in DataFrame
            #  reductions; see GH#28949
            ser = df.iloc[:, 0]

        # We do not get here with UDFs, so we know that our dtype
        #  should always be preserved by the implemented aggregations
        # TODO: Is this exactly right; see WrappedCythonOp get_result_dtype?
        res_values = self.grouper.agg_series(ser, alt, preserve_dtype=True)

        if isinstance(values, Categorical):
            # Because we only get here with known dtype-preserving
            #  reductions, we cast back to Categorical.
            # TODO: if we ever get "rank" working, exclude it here.
            res_values = type(values)._from_sequence(res_values, dtype=values.dtype)

        # If we are DataFrameGroupBy and went through a SeriesGroupByPath
        # then we need to reshape
        # GH#32223 includes case with IntegerArray values, ndarray res_values
        # test_groupby_duplicate_columns with object dtype values
        return ensure_block_shape(res_values, ndim=ndim)
