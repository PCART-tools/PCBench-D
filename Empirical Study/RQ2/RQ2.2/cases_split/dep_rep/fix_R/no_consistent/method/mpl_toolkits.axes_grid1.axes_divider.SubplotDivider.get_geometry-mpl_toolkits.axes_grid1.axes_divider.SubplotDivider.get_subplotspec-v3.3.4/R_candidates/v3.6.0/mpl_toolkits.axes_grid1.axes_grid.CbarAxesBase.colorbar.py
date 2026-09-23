    def colorbar(self, mappable, *, ticks=None, **kwargs):
        orientation = (
            "horizontal" if self.orientation in ["top", "bottom"] else
            "vertical")
        cb = self.figure.colorbar(mappable, cax=self, orientation=orientation,
                                  ticks=ticks, **kwargs)
        return cb
