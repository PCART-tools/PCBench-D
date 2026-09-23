    def get_window_extent(self, renderer=None):
        # docstring inherited
        if renderer is None:
            renderer = self.figure._get_renderer()
        bbox = self.get_bbox(renderer)
        try:  # Some subclasses redefine get_offset to take no args.
            px, py = self.get_offset(bbox, renderer)
        except TypeError:
            px, py = self.get_offset()
        return bbox.translated(px, py)
