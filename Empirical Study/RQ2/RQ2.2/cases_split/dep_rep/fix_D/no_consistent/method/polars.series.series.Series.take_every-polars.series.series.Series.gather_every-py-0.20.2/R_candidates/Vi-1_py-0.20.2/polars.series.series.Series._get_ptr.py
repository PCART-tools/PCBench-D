    def _get_ptr(self) -> tuple[int, int, int]:
        """
        Get a pointer to the start of the values buffer of a numeric Series.

        This will raise an error if the `Series` contains multiple chunks.

        This will return the offset, length and the pointer itself.

        """
        return self._s.get_ptr()
