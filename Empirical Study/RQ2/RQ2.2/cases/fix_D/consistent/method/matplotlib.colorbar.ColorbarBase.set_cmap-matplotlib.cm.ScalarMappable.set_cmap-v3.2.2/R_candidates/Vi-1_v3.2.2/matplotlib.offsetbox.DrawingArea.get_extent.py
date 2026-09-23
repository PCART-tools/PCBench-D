    def get_extent(self, renderer):
        """
        Return with, height, xdescent, ydescent of box
        """

        dpi_cor = renderer.points_to_pixels(1.)
        return (self.width * dpi_cor, self.height * dpi_cor,
                self.xdescent * dpi_cor, self.ydescent * dpi_cor)
