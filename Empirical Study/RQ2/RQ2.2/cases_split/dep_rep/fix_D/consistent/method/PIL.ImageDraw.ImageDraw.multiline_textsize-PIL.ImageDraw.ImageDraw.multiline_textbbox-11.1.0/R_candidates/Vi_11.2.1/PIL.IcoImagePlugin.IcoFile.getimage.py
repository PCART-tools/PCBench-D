    def getimage(self, size: tuple[int, int], bpp: int | bool = False) -> Image.Image:
        """
        Get an image from the icon
        """
        return self.frame(self.getentryindex(size, bpp))
