    def tobytes(self) -> bytes:
        """Convert palette to bytes.

        .. warning:: This method is experimental.
        """
        if self.rawmode:
            msg = "palette contains raw palette data"
            raise ValueError(msg)
        if isinstance(self.palette, bytes):
            return self.palette
        arr = array.array("B", self.palette)
        return arr.tobytes()
