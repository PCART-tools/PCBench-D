    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        return Bbox.union([child.get_window_extent(renderer)
                           for child in self.get_children()])
