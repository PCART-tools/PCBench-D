    def points_to_pixels(self, points):
        # docstring inherited
        return points * mpl_pt_to_in * self.dpi
