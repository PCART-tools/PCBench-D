    def __from_arrow__(self, array):
        """Construct IntervalArray from pyarrow Array/ChunkedArray."""
        import pyarrow
        from pandas.core.arrays import IntervalArray

        if isinstance(array, pyarrow.Array):
            chunks = [array]
        else:
            chunks = array.chunks

        results = []
        for arr in chunks:
            left = np.asarray(arr.storage.field("left"), dtype=self.subtype)
            right = np.asarray(arr.storage.field("right"), dtype=self.subtype)
            iarr = IntervalArray.from_arrays(left, right, closed=array.type.closed)
            results.append(iarr)

        return IntervalArray._concat_same_type(results)
