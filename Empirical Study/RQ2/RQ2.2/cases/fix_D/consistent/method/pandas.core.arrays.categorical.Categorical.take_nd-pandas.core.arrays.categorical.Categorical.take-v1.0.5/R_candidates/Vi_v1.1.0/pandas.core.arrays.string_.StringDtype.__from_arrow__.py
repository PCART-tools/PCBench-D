    def __from_arrow__(
        self, array: Union["pyarrow.Array", "pyarrow.ChunkedArray"]
    ) -> "StringArray":
        """
        Construct StringArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow  # noqa: F811

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

        return StringArray._concat_same_type(results)
