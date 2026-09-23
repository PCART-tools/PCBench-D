    def getpalette(self, rawmode: str | None = "RGB") -> list[int] | None:
        """
        Returns the image palette as a list.

        :param rawmode: The mode in which to return the palette. ``None`` will
           return the palette in its current mode.

           .. versionadded:: 9.1.0

        :returns: A list of color values [r, g, b, ...], or None if the
           image has no palette.
        """

        self.load()
        try:
            mode = self.im.getpalettemode()
        except ValueError:
            return None  # no palette
        if rawmode is None:
            rawmode = mode
        return list(self.im.getpalette(mode, rawmode))
