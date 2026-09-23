    def __bytes__(self):
        return b"[ " + b" ".join(pdf_repr(x) for x in self) + b" ]"
