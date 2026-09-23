    def draw(self, renderer):
        # docstring inherited
        self.image.draw(renderer)
        # bbox_artist(self, renderer, fill=False, props=dict(pad=0.))
        self.stale = False
