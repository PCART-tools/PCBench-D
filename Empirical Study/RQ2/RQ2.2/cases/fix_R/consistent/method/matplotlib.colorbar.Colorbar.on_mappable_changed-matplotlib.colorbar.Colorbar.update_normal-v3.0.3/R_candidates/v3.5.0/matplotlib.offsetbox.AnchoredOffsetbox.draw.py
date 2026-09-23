    def draw(self, renderer):
        # docstring inherited
        if not self.get_visible():
            return

        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        self._update_offset_func(renderer, fontsize)

        # update the location and size of the legend
        bbox = self.get_window_extent(renderer)
        self.update_frame(bbox, fontsize)
        self.patch.draw(renderer)

        width, height, xdescent, ydescent = self.get_extent(renderer)

        px, py = self.get_offset(width, height, xdescent, ydescent, renderer)

        self.get_child().set_offset((px, py))
        self.get_child().draw(renderer)
        self.stale = False
