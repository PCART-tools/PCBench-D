    def split(self):
        """
        Split this image into individual bands. This method returns a
        tuple of individual image bands from an image. For example,
        splitting an "RGB" image creates three new images each
        containing a copy of one of the original bands (red, green,
        blue).

        If you need only one band, :py:meth:`~PIL.Image.Image.getchannel`
        method can be more convenient and faster.

        :returns: A tuple containing bands.
        """

        self.load()
        if self.im.bands == 1:
            ims = [self.copy()]
        else:
            ims = map(self._new, self.im.split())
        return tuple(ims)
