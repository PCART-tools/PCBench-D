    def __init__(self, name: PdfName | bytes | str) -> None:
        if isinstance(name, PdfName):
            self.name = name.name
        elif isinstance(name, bytes):
            self.name = name
        else:
            self.name = name.encode("us-ascii")
