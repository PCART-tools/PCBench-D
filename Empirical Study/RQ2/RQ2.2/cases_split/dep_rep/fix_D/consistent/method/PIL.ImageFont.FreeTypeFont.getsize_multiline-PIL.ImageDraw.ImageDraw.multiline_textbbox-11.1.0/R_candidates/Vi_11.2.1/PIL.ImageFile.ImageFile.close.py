    def close(self) -> None:
        """
        Closes the file pointer, if possible.

        This operation will destroy the image core and release its memory.
        The image data will be unusable afterward.

        This function is required to close images that have multiple frames or
        have not had their file read and closed by the
        :py:meth:`~PIL.Image.Image.load` method. See :ref:`file-handling` for
        more information.
        """
        try:
            self._close_fp()
            self.fp = None
        except Exception as msg:
            logger.debug("Error closing: %s", msg)

        super().close()
