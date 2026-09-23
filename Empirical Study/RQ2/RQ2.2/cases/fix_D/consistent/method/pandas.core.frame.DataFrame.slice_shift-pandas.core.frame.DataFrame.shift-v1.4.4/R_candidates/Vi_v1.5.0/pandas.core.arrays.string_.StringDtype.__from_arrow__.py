    def __from_arrow__(
        self, array: pyarrow.Array | pyarrow.ChunkedArray
    ) -> BaseStringArray:
        """
        Construct StringArray from pyarrow Array/ChunkedArray.
        """
        if self.storage == "pyarrow":
            from pandas.core.arrays.string_arrow import ArrowStringArray

            return ArrowStringArray(array)
        else:

            import pyarrow

            if isinstance(array, pyarrow.Array):
                chunks = [array]
            else:
                # pyarrow.ChunkedArray
                chunks = array.chunks

            results = []
            for arr in chunks:
                # using _from_sequence to ensure None is converted to NA
                str_arr = StringArray._from_sequence(np.array(arr))
                results.append(str_arr)

        if results:
            return StringArray._concat_same_type(results)
        else:
            return StringArray(np.array([], dtype="object"))
