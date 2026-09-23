    def draw_frame(self, renderer):
        # update the location and size of the legend
        bbox = self.get_window_extent(renderer)
        self.update_frame(bbox)

        if self._drawFrame:
            self.patch.draw(renderer)
