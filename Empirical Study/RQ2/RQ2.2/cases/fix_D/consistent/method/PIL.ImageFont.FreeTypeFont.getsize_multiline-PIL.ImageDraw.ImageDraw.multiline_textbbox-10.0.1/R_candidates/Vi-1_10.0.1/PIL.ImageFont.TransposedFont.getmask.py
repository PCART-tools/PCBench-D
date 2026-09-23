    def getmask(self, text, mode="", *args, **kwargs):
        im = self.font.getmask(text, mode, *args, **kwargs)
        if self.orientation is not None:
            return im.transpose(self.orientation)
        return im
