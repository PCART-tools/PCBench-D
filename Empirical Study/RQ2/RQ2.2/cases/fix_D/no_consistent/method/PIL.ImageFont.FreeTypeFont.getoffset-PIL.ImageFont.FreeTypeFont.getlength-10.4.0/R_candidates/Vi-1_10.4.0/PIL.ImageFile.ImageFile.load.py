    def load(self):
        """Load image data based on tile list"""

        if self.tile is None:
            msg = "cannot load this image"
            raise OSError(msg)

        pixel = Image.Image.load(self)
        if not self.tile:
            return pixel

        self.map = None
        use_mmap = self.filename and len(self.tile) == 1
        # As of pypy 2.1.0, memory mapping was failing here.
        use_mmap = use_mmap and not hasattr(sys, "pypy_version_info")

        readonly = 0

        # look for read/seek overrides
        try:
            read = self.load_read
            # don't use mmap if there are custom read/seek functions
            use_mmap = False
        except AttributeError:
            read = self.fp.read

        try:
            seek = self.load_seek
            use_mmap = False
        except AttributeError:
            seek = self.fp.seek

        if use_mmap:
            # try memory mapping
            decoder_name, extents, offset, args = self.tile[0]
            if isinstance(args, str):
                args = (args, 0, 1)
            if (
                decoder_name == "raw"
                and len(args) >= 3
                and args[0] == self.mode
                and args[0] in Image._MAPMODES
            ):
                try:
                    # use mmap, if possible
                    import mmap

                    with open(self.filename) as fp:
                        self.map = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
                    if offset + self.size[1] * args[1] > self.map.size():
                        msg = "buffer is not large enough"
                        raise OSError(msg)
                    self.im = Image.core.map_buffer(
                        self.map, self.size, decoder_name, offset, args
                    )
                    readonly = 1
                    # After trashing self.im,
                    # we might need to reload the palette data.
                    if self.palette:
                        self.palette.dirty = 1
                except (AttributeError, OSError, ImportError):
                    self.map = None

        self.load_prepare()
        err_code = -3  # initialize to unknown error
        if not self.map:
            # sort tiles in file order
            self.tile.sort(key=_tilesort)

            try:
                # FIXME: This is a hack to handle TIFF's JpegTables tag.
                prefix = self.tile_prefix
            except AttributeError:
                prefix = b""

            # Remove consecutive duplicates that only differ by their offset
            self.tile = [
                list(tiles)[-1]
                for _, tiles in itertools.groupby(
                    self.tile, lambda tile: (tile[0], tile[1], tile[3])
                )
            ]
            for decoder_name, extents, offset, args in self.tile:
                seek(offset)
                decoder = Image._getdecoder(
                    self.mode, decoder_name, args, self.decoderconfig
                )
                try:
                    decoder.setimage(self.im, extents)
                    if decoder.pulls_fd:
                        decoder.setfd(self.fp)
                        err_code = decoder.decode(b"")[1]
                    else:
                        b = prefix
                        while True:
                            try:
                                s = read(self.decodermaxblock)
                            except (IndexError, struct.error) as e:
                                # truncated png/gif
                                if LOAD_TRUNCATED_IMAGES:
                                    break
                                else:
                                    msg = "image file is truncated"
                                    raise OSError(msg) from e

                            if not s:  # truncated jpeg
                                if LOAD_TRUNCATED_IMAGES:
                                    break
                                else:
                                    msg = (
                                        "image file is truncated "
                                        f"({len(b)} bytes not processed)"
                                    )
                                    raise OSError(msg)

                            b = b + s
                            n, err_code = decoder.decode(b)
                            if n < 0:
                                break
                            b = b[n:]
                finally:
                    # Need to cleanup here to prevent leaks
                    decoder.cleanup()

        self.tile = []
        self.readonly = readonly

        self.load_end()

        if self._exclusive_fp and self._close_exclusive_fp_after_loading:
            self.fp.close()
        self.fp = None

        if not self.map and not LOAD_TRUNCATED_IMAGES and err_code < 0:
            # still raised if decoder fails to return anything
            raise _get_oserror(err_code, encoder=False)

        return Image.Image.load(self)
