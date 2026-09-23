    def __from_arrow__(
        self, array: pyarrow.Array | pyarrow.ChunkedArray
    ) -> BooleanArray:
        """
        Construct BooleanArray from pyarrow Array/ChunkedArray.
        """
        import pyarrow

        if array.type != pyarrow.bool_() and not pyarrow.types.is_null(array.type):
            raise TypeError(f"Expected array of boolean type, got {array.type} instead")

        if isinstance(array, pyarrow.Array):
            chunks = [array]
            length = len(array)
        else:
            # pyarrow.ChunkedArray
            chunks = array.chunks
            length = array.length()

        if pyarrow.types.is_null(array.type):
            mask = np.ones(length, dtype=bool)
            # No need to init data, since all null
            data = np.empty(length, dtype=bool)
            return BooleanArray(data, mask)

        results = []
        for arr in chunks:
            buflist = arr.buffers()
            data = pyarrow.BooleanArray.from_buffers(
                arr.type, len(arr), [None, buflist[1]], offset=arr.offset
            ).to_numpy(zero_copy_only=False)
            if arr.null_count != 0:
                mask = pyarrow.BooleanArray.from_buffers(
                    arr.type, len(arr), [None, buflist[0]], offset=arr.offset
                ).to_numpy(zero_copy_only=False)
                mask = ~mask
            else:
                mask = np.zeros(len(arr), dtype=bool)

            bool_arr = BooleanArray(data, mask)
            results.append(bool_arr)

        if not results:
            return BooleanArray(
                np.array([], dtype=np.bool_), np.array([], dtype=np.bool_)
            )
        else:
            return BooleanArray._concat_same_type(results)
