    @classmethod
    def from_pdf_stream(cls, data):
        return cls(PdfParser.interpret_name(data))
