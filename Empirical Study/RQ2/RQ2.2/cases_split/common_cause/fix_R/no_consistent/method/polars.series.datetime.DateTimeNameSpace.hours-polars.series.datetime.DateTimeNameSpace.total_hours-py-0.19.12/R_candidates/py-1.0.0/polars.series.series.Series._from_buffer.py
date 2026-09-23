    @classmethod
    def _from_buffer(
        cls, dtype: PolarsDataType, buffer_info: BufferInfo, owner: Any
    ) -> Self:
        """
        Construct a Series from information about its underlying buffer.

        Parameters
        ----------
        dtype
            The data type of the buffer.
            Must be a physical type (integer, float, or boolean).
        buffer_info
            Tuple containing buffer information in the form `(pointer, offset, length)`.
        owner
            The object owning the buffer.

        Returns
        -------
        Series

        Raises
        ------
        TypeError
            When the given `dtype` is not supported.

        Notes
        -----
        This method is mainly intended for use with the dataframe interchange protocol.
        """
        return cls._from_pyseries(PySeries._from_buffer(dtype, buffer_info, owner))
