    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        width, height = renderer.get_canvas_width_height()
        bbox_in = self.get_window_extent(renderer).frozen()
        bbox_in._points /= [width, height]
        bbox_out = self.get_window_extent(renderer)
        clip = Bbox([[0, 0], [width, height]])
        self._transform = BboxTransform(Bbox([[0, 0], [1, 1]]), clip)
        return self._make_image(
            self._A,
            bbox_in, bbox_out, clip, magnification, unsampled=unsampled)
