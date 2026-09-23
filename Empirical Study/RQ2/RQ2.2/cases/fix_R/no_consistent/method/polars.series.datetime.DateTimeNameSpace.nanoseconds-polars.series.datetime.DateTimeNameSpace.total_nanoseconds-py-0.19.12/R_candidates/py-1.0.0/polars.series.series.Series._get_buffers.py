    def _get_buffers(self) -> SeriesBuffers:
        """
        Return the underlying values, validity, and offsets buffers as Series.

        The values buffer always exists.
        The validity buffer may not exist if the column contains no null values.
        The offsets buffer only exists for Series of data type `String` and `List`.

        Returns
        -------
        dict
            Dictionary with `"values"`, `"validity"`, and `"offsets"` keys mapping
            to the corresponding buffer or `None` if the buffer doesn't exist.

        Warnings
        --------
        The underlying buffers for `String` Series cannot be represented in this
        format. Instead, the buffers are converted to a values and offsets buffer.

        Notes
        -----
        This method is mainly intended for use with the dataframe interchange protocol.
        """
        buffers = self._s._get_buffers()
        keys = ("values", "validity", "offsets")
        return {  # type: ignore[return-value]
            k: self._from_pyseries(b) if b is not None else b
            for k, b in zip(keys, buffers)
        }
