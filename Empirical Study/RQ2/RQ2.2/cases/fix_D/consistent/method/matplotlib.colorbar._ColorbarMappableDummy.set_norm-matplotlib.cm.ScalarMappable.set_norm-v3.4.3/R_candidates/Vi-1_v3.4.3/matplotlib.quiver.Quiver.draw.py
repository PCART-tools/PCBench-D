    @martist.allow_rasterization
    def draw(self, renderer):
        self._init()
        verts = self._make_verts(self.U, self.V, self.angles)
        self.set_verts(verts, closed=False)
        self._new_UV = False
        super().draw(renderer)
        self.stale = False
