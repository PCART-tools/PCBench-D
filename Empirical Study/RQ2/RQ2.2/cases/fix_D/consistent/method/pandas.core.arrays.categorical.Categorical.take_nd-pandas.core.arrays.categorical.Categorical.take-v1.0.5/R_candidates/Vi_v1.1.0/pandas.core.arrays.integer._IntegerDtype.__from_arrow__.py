    def __from_arrow__(
        self, array: Union["pyarrow.Array", "pyarrow.ChunkedArray"]
    ) -> "IntegerArray":
        """
        Construct IntegerArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow  # noqa: F811
        from pandas.core.arrays._arrow_utils import pyarrow_array_to_numpy_and_mask

        pyarrow_type = pyarrow.from_numpy_dtype(self.type)
        if not array.type.equals(pyarrow_type):
            array = array.cast(pyarrow_type)

        if isinstance(array, pyarrow.Array):
            chunks = [array]
        else:
            # pyarrow.ChunkedArray
            chunks = array.chunks

        results = []
        for arr in chunks:
            data, mask = pyarrow_array_to_numpy_and_mask(arr, dtype=self.type)
            int_arr = IntegerArray(data.copy(), ~mask, copy=False)
            results.append(int_arr)

        return IntegerArray._concat_same_type(results)
