    def __init__(self, id, len, file, extra=None, png=None):
        """id: object id of stream; len: an unused Reference object for the
        length of the stream, or None (to use a memory buffer); file:
        a PdfFile; extra: a dictionary of extra key-value pairs to
        include in the stream header; png: if the data is already
        png compressed, the decode parameters"""
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
        if rcParams['pdf.compression'] and not png:
            self.compressobj = zlib.compressobj(rcParams['pdf.compression'])
        if self.len is None:
            self.file = BytesIO()
        else:
            self._writeHeader()
            self.pos = self.file.tell()
