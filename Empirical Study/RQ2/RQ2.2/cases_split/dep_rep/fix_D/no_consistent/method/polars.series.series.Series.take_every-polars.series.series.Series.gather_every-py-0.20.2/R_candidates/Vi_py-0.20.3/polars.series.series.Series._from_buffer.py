    @classmethod
    def _from_buffer(
        self, dtype: PolarsDataType, buffer_info: BufferInfo, owner: Any
    ) -> Self:
        """
        Construct a Series from information about its underlying buffer.

        Parameters
        ----------
        dtype
            The data type of the buffer.
        buffer_info
            Tuple containing buffer information in the form `(pointer, offset, length)`.
        owner
            The object owning the buffer.

        Returns
        -------
        Series
        """
        return self._from_pyseries(PySeries._from_buffer(dtype, buffer_info, owner))
