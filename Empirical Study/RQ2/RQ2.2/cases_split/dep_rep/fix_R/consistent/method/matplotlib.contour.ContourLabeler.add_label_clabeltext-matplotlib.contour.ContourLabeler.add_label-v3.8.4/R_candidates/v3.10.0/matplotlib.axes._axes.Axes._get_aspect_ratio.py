    def _get_aspect_ratio(self):
        """
        Convenience method to calculate the aspect ratio of the Axes in
        the display coordinate system.
        """
        figure_size = self.get_figure().get_size_inches()
        ll, ur = self.get_position() * figure_size
        width, height = ur - ll
        return height / (width * self.get_data_ratio())
