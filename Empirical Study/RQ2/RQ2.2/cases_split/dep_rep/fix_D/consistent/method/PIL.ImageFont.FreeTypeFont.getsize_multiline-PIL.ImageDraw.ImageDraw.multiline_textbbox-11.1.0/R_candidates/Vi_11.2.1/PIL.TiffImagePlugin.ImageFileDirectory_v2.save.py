    def save(self, fp: IO[bytes]) -> int:
        if fp.tell() == 0:  # skip TIFF header on subsequent pages
            fp.write(self._get_ifh())

        offset = fp.tell()
        result = self.tobytes(offset)
        fp.write(result)
        return offset + len(result)
