    def frombytes(
        self, data: bytes | bytearray, decoder_name: str = "raw", *args: Any
    ) -> None:
        """
        Loads this image with pixel data from a bytes object.

        This method is similar to the :py:func:`~PIL.Image.frombytes` function,
        but loads data into this image instead of creating a new image object.
        """

        if self.width == 0 or self.height == 0:
            return

        decoder_args: Any = args
        if len(decoder_args) == 1 and isinstance(decoder_args[0], tuple):
            # may pass tuple instead of argument list
            decoder_args = decoder_args[0]

        # default format
        if decoder_name == "raw" and decoder_args == ():
            decoder_args = self.mode

        # unpack data
        d = _getdecoder(self.mode, decoder_name, decoder_args)
        d.setimage(self.im)
        s = d.decode(data)

        if s[0] >= 0:
            msg = "not enough image data"
            raise ValueError(msg)
        if s[1] != 0:
            msg = "cannot decode image data"
            raise ValueError(msg)
