    def grid2mask(self, xi, yi):
        """Return nearest space in mask-coords from given grid-coords."""
        return (int(xi * self.x_grid2mask + 0.5),
                int(yi * self.y_grid2mask + 0.5))
