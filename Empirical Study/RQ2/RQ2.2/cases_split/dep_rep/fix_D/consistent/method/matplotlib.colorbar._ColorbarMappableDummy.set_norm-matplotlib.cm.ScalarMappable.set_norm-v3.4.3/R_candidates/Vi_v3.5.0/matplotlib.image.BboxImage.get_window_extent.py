    def get_window_extent(self, renderer=None):
        if renderer is None:
            renderer = self.get_figure()._cachedRenderer

        if isinstance(self.bbox, BboxBase):
            return self.bbox
        elif callable(self.bbox):
            return self.bbox(renderer)
        else:
            raise ValueError("Unknown type of bbox")
