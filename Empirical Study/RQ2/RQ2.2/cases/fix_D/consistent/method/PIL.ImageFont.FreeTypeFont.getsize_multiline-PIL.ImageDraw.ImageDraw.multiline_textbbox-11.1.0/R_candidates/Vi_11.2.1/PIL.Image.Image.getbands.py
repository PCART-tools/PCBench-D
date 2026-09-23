    def getbands(self) -> tuple[str, ...]:
        """
        Returns a tuple containing the name of each band in this image.
        For example, ``getbands`` on an RGB image returns ("R", "G", "B").

        :returns: A tuple containing band names.
        :rtype: tuple
        """
        return ImageMode.getmode(self.mode).bands
