    def set_as_raw(
        self, data: bytes, rawmode: str | None = None, extra: tuple[Any, ...] = ()
    ) -> None:
        """
        Convenience method to set the internal image from a stream of raw data

        :param data: Bytes to be set
        :param rawmode: The rawmode to be used for the decoder.
            If not specified, it will default to the mode of the image
        :param extra: Extra arguments for the decoder.
        :returns: None
        """

        if not rawmode:
            rawmode = self.mode
        d = Image._getdecoder(self.mode, "raw", rawmode, extra)
        assert self.im is not None
        d.setimage(self.im, self.state.extents())
        s = d.decode(data)

        if s[0] >= 0:
            msg = "not enough image data"
            raise ValueError(msg)
        if s[1] != 0:
            msg = "cannot decode image data"
            raise ValueError(msg)
