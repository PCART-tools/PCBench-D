    def new_gc(self):
        # docstring inherited
        DEBUG_MSG('new_gc()', 2, self)
        self.gc = GraphicsContextWx(self.bitmap, self)
        self.gc.select()
        self.gc.unselect()
        return self.gc
