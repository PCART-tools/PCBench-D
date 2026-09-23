    def getimage(self, size=None):
        if size is None:
            size = self.bestsize()
        if len(size) == 2:
            size = (size[0], size[1], 1)
        channels = self.dataforsize(size)

        im = channels.get("RGBA", None)
        if im:
            return im

        im = channels.get("RGB").copy()
        try:
            im.putalpha(channels["A"])
        except KeyError:
            pass
        return im
