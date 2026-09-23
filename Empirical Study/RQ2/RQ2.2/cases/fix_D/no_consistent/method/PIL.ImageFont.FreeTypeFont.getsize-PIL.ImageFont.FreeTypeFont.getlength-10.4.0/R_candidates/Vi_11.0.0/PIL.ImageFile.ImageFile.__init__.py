    def __init__(
        self, fp: StrOrBytesPath | IO[bytes], filename: str | bytes | None = None
    ) -> None:
        super().__init__()

        self._min_frame = 0

        self.custom_mimetype: str | None = None

        self.tile: list[_Tile] = []
        """ A list of tile descriptors, or ``None`` """

        self.readonly = 1  # until we know better

        self.decoderconfig: tuple[Any, ...] = ()
        self.decodermaxblock = MAXBLOCK

        if is_path(fp):
            # filename
            self.fp = open(fp, "rb")
            self.filename = os.path.realpath(os.fspath(fp))
            self._exclusive_fp = True
        else:
            # stream
            self.fp = cast(IO[bytes], fp)
            self.filename = filename if filename is not None else ""
            # can be overridden
            self._exclusive_fp = False

        try:
            try:
                self._open()
            except (
                IndexError,  # end of data
                TypeError,  # end of data (ord)
                KeyError,  # unsupported mode
                EOFError,  # got header but not the first frame
                struct.error,
            ) as v:
                raise SyntaxError(v) from v

            if not self.mode or self.size[0] <= 0 or self.size[1] <= 0:
                msg = "not identified by this driver"
                raise SyntaxError(msg)
        except BaseException:
            # close the file only if we have opened it this constructor
            if self._exclusive_fp:
                self.fp.close()
            raise
