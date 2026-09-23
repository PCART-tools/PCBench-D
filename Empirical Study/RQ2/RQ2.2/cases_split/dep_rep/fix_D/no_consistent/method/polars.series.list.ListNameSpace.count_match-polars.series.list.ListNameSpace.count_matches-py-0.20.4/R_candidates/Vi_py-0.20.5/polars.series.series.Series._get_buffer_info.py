    def _get_buffer_info(self) -> BufferInfo:
        """
        Return pointer, offset, and length information about the underlying buffer.

        Returns
        -------
        tuple of ints
            Tuple of the form (pointer, offset, length)

        Raises
        ------
        ComputeError
            If the `Series` contains multiple chunks.
        """
        return self._s._get_buffer_info()
