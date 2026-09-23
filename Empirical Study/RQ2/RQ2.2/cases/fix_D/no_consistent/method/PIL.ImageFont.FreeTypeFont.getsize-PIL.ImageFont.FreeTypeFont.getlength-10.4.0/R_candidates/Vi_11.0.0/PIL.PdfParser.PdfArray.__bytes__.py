    def __bytes__(self) -> bytes:
        return b"[ " + b" ".join(pdf_repr(x) for x in self) + b" ]"
