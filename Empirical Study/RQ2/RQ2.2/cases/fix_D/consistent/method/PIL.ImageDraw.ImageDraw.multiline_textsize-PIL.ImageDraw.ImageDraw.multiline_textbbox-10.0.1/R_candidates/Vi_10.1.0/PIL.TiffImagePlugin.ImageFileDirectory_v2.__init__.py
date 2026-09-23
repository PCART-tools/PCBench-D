    def __init__(self, ifh=b"II\052\0\0\0\0\0", prefix=None, group=None):
        """Initialize an ImageFileDirectory.

        To construct an ImageFileDirectory from a real file, pass the 8-byte
        magic header to the constructor.  To only set the endianness, pass it
        as the 'prefix' keyword argument.

        :param ifh: One of the accepted magic headers (cf. PREFIXES); also sets
              endianness.
        :param prefix: Override the endianness of the file.
        """
        if not _accept(ifh):
            msg = f"not a TIFF file (header {repr(ifh)} not valid)"
            raise SyntaxError(msg)
        self._prefix = prefix if prefix is not None else ifh[:2]
        if self._prefix == MM:
            self._endian = ">"
        elif self._prefix == II:
            self._endian = "<"
        else:
            msg = "not a TIFF IFD"
            raise SyntaxError(msg)
        self._bigtiff = ifh[2] == 43
        self.group = group
        self.tagtype = {}
        """ Dictionary of tag types """
        self.reset()
        (self.next,) = (
            self._unpack("Q", ifh[8:]) if self._bigtiff else self._unpack("L", ifh[4:])
        )
        self._legacy_api = False
