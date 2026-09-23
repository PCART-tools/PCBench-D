    def redraw_in_frame(self):
        """
        This method can only be used after an initial draw which
        caches the renderer.  It is used to efficiently update Axes
        data (axis ticks, labels, etc are not updated)
        """
        if self.figure._cachedRenderer is None:
            raise AttributeError("redraw_in_frame can only be used after an "
                                 "initial draw which caches the renderer")
        self.draw(self.figure._cachedRenderer, inframe=True)
