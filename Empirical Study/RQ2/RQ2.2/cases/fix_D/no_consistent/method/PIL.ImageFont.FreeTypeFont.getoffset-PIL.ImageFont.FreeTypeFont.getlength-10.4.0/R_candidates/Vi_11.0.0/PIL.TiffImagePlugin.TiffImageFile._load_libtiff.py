    def _load_libtiff(self) -> Image.core.PixelAccess | None:
        """Overload method triggered when we detect a compressed tiff
        Calls out to libtiff"""

        Image.Image.load(self)

        self.load_prepare()

        if not len(self.tile) == 1:
            msg = "Not exactly one tile"
            raise OSError(msg)

        # (self._compression, (extents tuple),
        #   0, (rawmode, self._compression, fp))
        extents = self.tile[0][1]
        args = self.tile[0][3]

        # To be nice on memory footprint, if there's a
        # file descriptor, use that instead of reading
        # into a string in python.
        try:
            fp = hasattr(self.fp, "fileno") and self.fp.fileno()
            # flush the file descriptor, prevents error on pypy 2.4+
            # should also eliminate the need for fp.tell
            # in _seek
            if hasattr(self.fp, "flush"):
                self.fp.flush()
        except OSError:
            # io.BytesIO have a fileno, but returns an OSError if
            # it doesn't use a file descriptor.
            fp = False

        if fp:
            assert isinstance(args, tuple)
            args_list = list(args)
            args_list[2] = fp
            args = tuple(args_list)

        decoder = Image._getdecoder(self.mode, "libtiff", args, self.decoderconfig)
        try:
            decoder.setimage(self.im, extents)
        except ValueError as e:
            msg = "Couldn't set the image"
            raise OSError(msg) from e

        close_self_fp = self._exclusive_fp and not self.is_animated
        if hasattr(self.fp, "getvalue"):
            # We've got a stringio like thing passed in. Yay for all in memory.
            # The decoder needs the entire file in one shot, so there's not
            # a lot we can do here other than give it the entire file.
            # unless we could do something like get the address of the
            # underlying string for stringio.
            #
            # Rearranging for supporting byteio items, since they have a fileno
            # that returns an OSError if there's no underlying fp. Easier to
            # deal with here by reordering.
            logger.debug("have getvalue. just sending in a string from getvalue")
            n, err = decoder.decode(self.fp.getvalue())
        elif fp:
            # we've got a actual file on disk, pass in the fp.
            logger.debug("have fileno, calling fileno version of the decoder.")
            if not close_self_fp:
                self.fp.seek(0)
            # 4 bytes, otherwise the trace might error out
            n, err = decoder.decode(b"fpfp")
        else:
            # we have something else.
            logger.debug("don't have fileno or getvalue. just reading")
            self.fp.seek(0)
            # UNDONE -- so much for that buffer size thing.
            n, err = decoder.decode(self.fp.read())

        self.tile = []
        self.readonly = 0

        self.load_end()

        if close_self_fp:
            self.fp.close()
            self.fp = None  # might be shared

        if err < 0:
            raise OSError(err)

        return Image.Image.load(self)
