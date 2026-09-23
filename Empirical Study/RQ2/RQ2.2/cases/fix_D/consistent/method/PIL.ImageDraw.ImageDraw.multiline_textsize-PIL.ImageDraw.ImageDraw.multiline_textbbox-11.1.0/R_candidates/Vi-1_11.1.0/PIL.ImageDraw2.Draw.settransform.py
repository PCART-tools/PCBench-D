    def settransform(self, offset: tuple[float, float]) -> None:
        """Sets a transformation offset."""
        (xoffset, yoffset) = offset
        self.transform = (1, 0, xoffset, 0, 1, yoffset)
