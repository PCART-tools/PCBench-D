    def getmask(
        self, text: str | bytes, mode: str = "", *args: Any, **kwargs: Any
    ) -> Image.core.ImagingCore:
        im = self.font.getmask(text, mode, *args, **kwargs)
        if self.orientation is not None:
            return im.transpose(self.orientation)
        return im
