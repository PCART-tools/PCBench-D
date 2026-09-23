    @classmethod
    def frombytes(cls, data: bytes) -> GimpPaletteFile:
        self = cls.__new__(cls)
        self._read(BytesIO(data), False)
        return self
