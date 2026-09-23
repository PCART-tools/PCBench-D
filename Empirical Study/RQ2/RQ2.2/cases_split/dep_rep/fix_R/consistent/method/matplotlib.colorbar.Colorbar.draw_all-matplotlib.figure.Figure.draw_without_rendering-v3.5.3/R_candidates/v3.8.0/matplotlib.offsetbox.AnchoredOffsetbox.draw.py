    def draw(self, renderer):
        # docstring inherited
        if not self.get_visible():
            return

        # update the location and size of the legend
        bbox = self.get_window_extent(renderer)
        fontsize = renderer.points_to_pixels(self.prop.get_size_in_points())
        self.update_frame(bbox, fontsize)
        self.patch.draw(renderer)

        px, py = self.get_offset(self.get_bbox(renderer), renderer)
        self.get_child().set_offset((px, py))
        self.get_child().draw(renderer)
        self.stale = False
