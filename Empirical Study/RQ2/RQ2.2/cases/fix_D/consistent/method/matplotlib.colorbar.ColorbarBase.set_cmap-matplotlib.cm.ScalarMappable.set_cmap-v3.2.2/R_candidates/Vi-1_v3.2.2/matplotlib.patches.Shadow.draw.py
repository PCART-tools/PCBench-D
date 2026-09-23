    def draw(self, renderer):
        self._update_transform(renderer)
        Patch.draw(self, renderer)
