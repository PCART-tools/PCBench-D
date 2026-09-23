    def __from_arrow__(
        self, array: pyarrow.Array | pyarrow.ChunkedArray
    ) -> PeriodArray:
        """
        Construct PeriodArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow

        from pandas.core.arrays import PeriodArray
        from pandas.core.arrays._arrow_utils import pyarrow_array_to_numpy_and_mask

        if isinstance(array, pyarrow.Array):
            chunks = [array]
        else:
            chunks = array.chunks

        results = []
        for arr in chunks:
            data, mask = pyarrow_array_to_numpy_and_mask(arr, dtype="int64")
            parr = PeriodArray(data.copy(), freq=self.freq, copy=False)
            parr[~mask] = NaT
            results.append(parr)

        if not results:
            return PeriodArray(np.array([], dtype="int64"), freq=self.freq, copy=False)
        return PeriodArray._concat_same_type(results)
