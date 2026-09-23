    def draw_frame(self, renderer):
        # update the location and size of the legend
        self.update_frame(self.get_window_extent(renderer))
        self.patch.draw(renderer)
