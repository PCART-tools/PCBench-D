    def new_gc(self):
        # docstring inherited
        _log.debug("%s - new_gc()", type(self))
        self.gc = GraphicsContextWx(self.bitmap, self)
        self.gc.select()
        self.gc.unselect()
        return self.gc
