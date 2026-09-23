    def __init__(self, fp, charset_encoding="iso8859-1"):
        self.charset_encoding = charset_encoding

        magic = l32(fp.read(4))
        if magic != PCF_MAGIC:
            msg = "not a PCF file"
            raise SyntaxError(msg)

        super().__init__()

        count = l32(fp.read(4))
        self.toc = {}
        for i in range(count):
            type = l32(fp.read(4))
            self.toc[type] = l32(fp.read(4)), l32(fp.read(4)), l32(fp.read(4))

        self.fp = fp

        self.info = self._load_properties()

        metrics = self._load_metrics()
        bitmaps = self._load_bitmaps(metrics)
        encoding = self._load_encoding()

        #
        # create glyph structure

        for ch, ix in enumerate(encoding):
            if ix is not None:
                (
                    xsize,
                    ysize,
                    left,
                    right,
                    width,
                    ascent,
                    descent,
                    attributes,
                ) = metrics[ix]
                self.glyph[ch] = (
                    (width, 0),
                    (left, descent - ysize, xsize + left, descent),
                    (0, 0, xsize, ysize),
                    bitmaps[ix],
                )
