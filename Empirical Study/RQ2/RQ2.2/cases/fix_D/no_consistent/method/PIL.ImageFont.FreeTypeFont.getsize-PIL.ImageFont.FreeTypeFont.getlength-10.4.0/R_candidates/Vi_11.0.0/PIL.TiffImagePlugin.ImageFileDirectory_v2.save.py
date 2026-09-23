    def save(self, fp: IO[bytes]) -> int:
        if fp.tell() == 0:  # skip TIFF header on subsequent pages
            # tiff header -- PIL always starts the first IFD at offset 8
            fp.write(self._prefix + self._pack("HL", 42, 8))

        offset = fp.tell()
        result = self.tobytes(offset)
        fp.write(result)
        return offset + len(result)
