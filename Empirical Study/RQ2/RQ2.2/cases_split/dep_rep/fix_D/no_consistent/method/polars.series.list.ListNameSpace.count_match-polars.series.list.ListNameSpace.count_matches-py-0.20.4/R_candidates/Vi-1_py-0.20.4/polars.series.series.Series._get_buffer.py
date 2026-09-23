    def _get_buffer(self, index: Literal[0, 1, 2]) -> Self | None:
        """
        Return the underlying data, validity, or offsets buffer as a Series.

        The data buffer always exists.
        The validity buffer may not exist if the column contains no null values.
        The offsets buffer only exists for Series of data type `String` and `List`.

        Parameters
        ----------
        index
            An index indicating the buffer to return:

            - `0` -> data buffer
            - `1` -> validity buffer
            - `2` -> offsets buffer

        Returns
        -------
        Series or None
            `Series` if the specified buffer exists, `None` otherwise.

        Raises
        ------
        ComputeError
            If the `Series` contains multiple chunks.
        """
        buffer = self._s._get_buffer(index)
        if buffer is None:
            return None
        return self._from_pyseries(buffer)
