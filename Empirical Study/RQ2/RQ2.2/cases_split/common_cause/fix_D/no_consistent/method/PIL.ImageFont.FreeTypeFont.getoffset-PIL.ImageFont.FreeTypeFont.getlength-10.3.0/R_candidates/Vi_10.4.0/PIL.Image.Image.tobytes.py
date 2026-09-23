    def tobytes(self, encoder_name: str = "raw", *args: Any) -> bytes:
        """
        Return image as a bytes object.

        .. warning::

            This method returns the raw image data from the internal
            storage.  For compressed image data (e.g. PNG, JPEG) use
            :meth:`~.save`, with a BytesIO parameter for in-memory
            data.

        :param encoder_name: What encoder to use.  The default is to
                             use the standard "raw" encoder.

                             A list of C encoders can be seen under
                             codecs section of the function array in
                             :file:`_imaging.c`. Python encoders are
                             registered within the relevant plugins.
        :param args: Extra arguments to the encoder.
        :returns: A :py:class:`bytes` object.
        """

        encoder_args: Any = args
        if len(encoder_args) == 1 and isinstance(encoder_args[0], tuple):
            # may pass tuple instead of argument list
            encoder_args = encoder_args[0]

        if encoder_name == "raw" and encoder_args == ():
            encoder_args = self.mode

        self.load()

        if self.width == 0 or self.height == 0:
            return b""

        # unpack data
        e = _getencoder(self.mode, encoder_name, encoder_args)
        e.setimage(self.im)

        bufsize = max(65536, self.size[0] * 4)  # see RawEncode.c

        output = []
        while True:
            bytes_consumed, errcode, data = e.encode(bufsize)
            output.append(data)
            if errcode:
                break
        if errcode < 0:
            msg = f"encoder error {errcode} in tobytes"
            raise RuntimeError(msg)

        return b"".join(output)
