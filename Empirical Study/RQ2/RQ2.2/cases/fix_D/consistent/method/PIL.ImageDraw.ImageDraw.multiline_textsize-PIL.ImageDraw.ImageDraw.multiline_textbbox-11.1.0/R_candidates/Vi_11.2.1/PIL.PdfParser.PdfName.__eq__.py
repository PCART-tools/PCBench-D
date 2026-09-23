    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, PdfName) and other.name == self.name
        ) or other == self.name
