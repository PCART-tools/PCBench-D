    def __from_arrow__(
        self, array: pyarrow.Array | pyarrow.ChunkedArray
    ) -> BaseStringArray:
        """
        Construct StringArray from pyarrow Array/ChunkedArray.
        """
        if self.storage == "pyarrow":
            from pandas.core.arrays.string_arrow import ArrowStringArray

            return ArrowStringArray(array)
        elif self.storage == "pyarrow_numpy":
            from pandas.core.arrays.string_arrow import ArrowStringArrayNumpySemantics

            return ArrowStringArrayNumpySemantics(array)
        else:
            import pyarrow

            if isinstance(array, pyarrow.Array):
                chunks = [array]
            else:
                # pyarrow.ChunkedArray
                chunks = array.chunks

        if len(chunks) == 0:
            arr = np.array([], dtype=object)
        else:
            arr = pyarrow.concat_arrays(chunks).to_numpy(zero_copy_only=False)
            arr = ensure_string_array(arr, na_value=libmissing.NA)
        # Bypass validation inside StringArray constructor, see GH#47781
        new_string_array = StringArray.__new__(StringArray)
        NDArrayBacked.__init__(
            new_string_array,
            arr,
            StringDtype(storage="python"),
        )
        return new_string_array
