    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        """
        :param offset: Distance to seek.
        :param whence: Whether the distance is relative to the start,
                       end or current position.
        :returns: The resulting position, relative to the start.
        """
        if whence == os.SEEK_SET:
            offset += self.offsetOfNewPage

        self.f.seek(offset, whence)
        return self.tell()
