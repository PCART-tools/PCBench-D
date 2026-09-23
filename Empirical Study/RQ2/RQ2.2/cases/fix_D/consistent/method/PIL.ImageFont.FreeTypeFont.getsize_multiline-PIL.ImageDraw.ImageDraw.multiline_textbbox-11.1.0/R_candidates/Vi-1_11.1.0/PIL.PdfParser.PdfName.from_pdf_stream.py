    @classmethod
    def from_pdf_stream(cls, data: bytes) -> PdfName:
        return cls(PdfParser.interpret_name(data))
