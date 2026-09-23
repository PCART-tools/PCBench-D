    def frombytes(self, buffer: bytes) -> None:
        """
        Load display memory contents from byte data.

        :param buffer: A buffer containing display data (usually
                       data returned from :py:func:`~PIL.ImageWin.Dib.tobytes`)
        """
        self.image.frombytes(buffer)
