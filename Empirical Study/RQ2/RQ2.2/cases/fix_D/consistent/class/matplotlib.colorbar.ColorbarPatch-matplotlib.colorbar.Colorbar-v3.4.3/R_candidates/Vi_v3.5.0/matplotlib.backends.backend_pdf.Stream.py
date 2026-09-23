class Stream:
    """
    PDF stream object.

    This has no pdfRepr method. Instead, call begin(), then output the
    contents of the stream by calling write(), and finally call end().
    """
    __slots__ = ('id', 'len', 'pdfFile', 'file', 'compressobj', 'extra', 'pos')

    def __init__(self, id, len, file, extra=None, png=None):
        """
        Parameters
        ----------
        id : int
            Object id of the stream.
        len : Reference or None
            An unused Reference object for the length of the stream;
            None means to use a memory buffer so the length can be inlined.
        file : PdfFile
            The underlying object to write the stream to.
        extra : dict from Name to anything, or None
            Extra key-value pairs to include in the stream header.
        png : dict or None
            If the data is already png encoded, the decode parameters.
        """
        self.id = id            # object id
        self.len = len          # id of length object
        self.pdfFile = file
        self.file = file.fh      # file to which the stream is written
        self.compressobj = None  # compression object
        if extra is None:
            self.extra = dict()
        else:
            self.extra = extra.copy()
        if png is not None:
            self.extra.update({'Filter':      Name('FlateDecode'),
                               'DecodeParms': png})

        self.pdfFile.recordXref(self.id)
        if mpl.rcParams['pdf.compression'] and not png:
            self.compressobj = zlib.compressobj(
                mpl.rcParams['pdf.compression'])
        if self.len is None:
            self.file = BytesIO()
        else:
            self._writeHeader()
            self.pos = self.file.tell()

    def _writeHeader(self):
        write = self.file.write
        write(b"%d 0 obj\n" % self.id)
        dict = self.extra
        dict['Length'] = self.len
        if mpl.rcParams['pdf.compression']:
            dict['Filter'] = Name('FlateDecode')

        write(pdfRepr(dict))
        write(b"\nstream\n")

    def end(self):
        """Finalize stream."""

        self._flush()
        if self.len is None:
            contents = self.file.getvalue()
            self.len = len(contents)
            self.file = self.pdfFile.fh
            self._writeHeader()
            self.file.write(contents)
            self.file.write(b"\nendstream\nendobj\n")
        else:
            length = self.file.tell() - self.pos
            self.file.write(b"\nendstream\nendobj\n")
            self.pdfFile.writeObject(self.len, length)

    def write(self, data):
        """Write some data on the stream."""

        if self.compressobj is None:
            self.file.write(data)
        else:
            compressed = self.compressobj.compress(data)
            self.file.write(compressed)

    def _flush(self):
        """Flush the compression object."""

        if self.compressobj is not None:
            compressed = self.compressobj.flush()
            self.file.write(compressed)
            self.compressobj = None
