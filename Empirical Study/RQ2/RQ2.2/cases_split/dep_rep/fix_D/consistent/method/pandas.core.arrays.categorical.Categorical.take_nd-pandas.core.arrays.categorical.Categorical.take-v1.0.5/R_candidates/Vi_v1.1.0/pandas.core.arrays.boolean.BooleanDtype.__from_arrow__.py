    def __from_arrow__(
        self, array: Union["pyarrow.Array", "pyarrow.ChunkedArray"]
    ) -> "BooleanArray":
        """
        Construct BooleanArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow  # noqa: F811

        if isinstance(array, pyarrow.Array):
            chunks = [array]
        else:
            # pyarrow.ChunkedArray
            chunks = array.chunks

        results = []
        for arr in chunks:
            # TODO should optimize this without going through object array
            bool_arr = BooleanArray._from_sequence(np.array(arr))
            results.append(bool_arr)

        return BooleanArray._concat_same_type(results)
