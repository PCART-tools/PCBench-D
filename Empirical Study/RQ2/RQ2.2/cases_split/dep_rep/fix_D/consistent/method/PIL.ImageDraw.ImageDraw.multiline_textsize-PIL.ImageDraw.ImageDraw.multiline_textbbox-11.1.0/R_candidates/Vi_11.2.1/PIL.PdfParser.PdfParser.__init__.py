    def __init__(
        self,
        filename: str | None = None,
        f: IO[bytes] | None = None,
        buf: bytes | bytearray | None = None,
        start_offset: int = 0,
        mode: str = "rb",
    ) -> None:
        if buf and f:
            msg = "specify buf or f or filename, but not both buf and f"
            raise RuntimeError(msg)
        self.filename = filename
        self.buf: bytes | bytearray | mmap.mmap | None = buf
        self.f = f
        self.start_offset = start_offset
        self.should_close_buf = False
        self.should_close_file = False
        if filename is not None and f is None:
            self.f = f = open(filename, mode)
            self.should_close_file = True
        if f is not None:
            self.buf = self.get_buf_from_file(f)
            self.should_close_buf = True
            if not filename and hasattr(f, "name"):
                self.filename = f.name
        self.cached_objects: dict[IndirectReference, Any] = {}
        self.root_ref: IndirectReference | None
        self.info_ref: IndirectReference | None
        self.pages_ref: IndirectReference | None
        self.last_xref_section_offset: int | None
        if self.buf:
            self.read_pdf_info()
        else:
            self.file_size_total = self.file_size_this = 0
            self.root = PdfDict()
            self.root_ref = None
            self.info = PdfDict()
            self.info_ref = None
            self.page_tree_root = PdfDict()
            self.pages: list[IndirectReference] = []
            self.orig_pages: list[IndirectReference] = []
            self.pages_ref = None
            self.last_xref_section_offset = None
            self.trailer_dict: dict[bytes, Any] = {}
            self.xref_table = XrefTable()
        self.xref_table.reading_finished = True
        if f:
            self.seek_end()
