    def draw(self, renderer):
        # docstring inherited
        for c in self._children:
            c.draw(renderer)
        bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
