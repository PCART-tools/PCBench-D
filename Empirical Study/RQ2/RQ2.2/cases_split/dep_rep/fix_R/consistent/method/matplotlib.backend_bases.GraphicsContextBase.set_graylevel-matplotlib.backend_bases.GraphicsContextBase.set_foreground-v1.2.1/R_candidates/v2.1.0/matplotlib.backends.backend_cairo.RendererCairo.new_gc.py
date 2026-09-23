    def new_gc(self):
        self.gc.ctx.save()
        self.gc._alpha = 1.0
        self.gc._forced_alpha = False # if True, _alpha overrides A from RGBA
        return self.gc
