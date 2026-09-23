    def begin_document(self, id: str | None = None) -> None:
        """Set up printing of a document. (Write PostScript DSC header.)"""
        # FIXME: incomplete
        self.fp.write(
            b"%!PS-Adobe-3.0\n"
            b"save\n"
            b"/showpage { } def\n"
            b"%%EndComments\n"
            b"%%BeginDocument\n"
        )
        # self.fp.write(ERROR_PS)  # debugging!
        self.fp.write(EDROFF_PS)
        self.fp.write(VDI_PS)
        self.fp.write(b"%%EndProlog\n")
        self.isofont: dict[bytes, int] = {}
