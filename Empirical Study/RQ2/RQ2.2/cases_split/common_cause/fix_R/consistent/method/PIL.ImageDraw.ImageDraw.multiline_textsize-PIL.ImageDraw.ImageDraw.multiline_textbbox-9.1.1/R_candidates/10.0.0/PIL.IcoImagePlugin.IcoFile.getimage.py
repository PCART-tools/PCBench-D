    def getimage(self, size, bpp=False):
        """
        Get an image from the icon
        """
        return self.frame(self.getentryindex(size, bpp))
