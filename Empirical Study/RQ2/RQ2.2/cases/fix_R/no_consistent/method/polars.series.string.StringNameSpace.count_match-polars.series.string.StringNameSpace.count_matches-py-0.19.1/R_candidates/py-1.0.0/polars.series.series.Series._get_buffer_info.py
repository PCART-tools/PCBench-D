    def _get_buffer_info(self) -> BufferInfo:
        """
        Return pointer, offset, and length information about the underlying buffer.

        Returns
        -------
        tuple of ints
            Tuple of the form (pointer, offset, length)

        Raises
        ------
        TypeError
            If the `Series` data type is not physical.
        ComputeError
            If the `Series` contains multiple chunks.

        Notes
        -----
        This method is mainly intended for use with the dataframe interchange protocol.
        """
        return self._s._get_buffer_info()
