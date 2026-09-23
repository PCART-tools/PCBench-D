    def getimage(
        self, size: tuple[int, int] | tuple[int, int, int] | None = None
    ) -> Image.Image:
        if size is None:
            size = self.bestsize()
        elif len(size) == 2:
            size = (size[0], size[1], 1)
        channels = self.dataforsize(size)

        im = channels.get("RGBA")
        if im:
            return im

        im = channels["RGB"].copy()
        try:
            im.putalpha(channels["A"])
        except KeyError:
            pass
        return im
