    def getdata(self) -> tuple[str, Sequence[int] | bytes | bytearray]:
        """
        Get palette contents in format suitable for the low-level
        ``im.putpalette`` primitive.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            return self.rawmode, self.palette
        return self.mode, self.tobytes()
