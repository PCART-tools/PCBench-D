    def __init__(self, fp=None, filename=None):
        super().__init__()

        self._min_frame = 0

        self.custom_mimetype = None

        self.tile = None
        """ A list of tile descriptors, or ``None`` """

        self.readonly = 1  # until we know better

        self.decoderconfig = ()
        self.decodermaxblock = MAXBLOCK

        if is_path(fp):
            # filename
            self.fp = open(fp, "rb")
            self.filename = fp
            self._exclusive_fp = True
        else:
            # stream
            self.fp = fp
            self.filename = filename
            # can be overridden
            self._exclusive_fp = None

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
