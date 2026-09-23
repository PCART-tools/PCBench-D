    @artist.allow_rasterization
    def draw(self, renderer):
        self._set_transforms()
        Collection.draw(self, renderer)
