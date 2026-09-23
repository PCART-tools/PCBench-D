    def update_datalim_bounds(self, bounds):
        """
        Extend the `~.Axes.datalim` BBox to include the given
        `~matplotlib.transforms.Bbox`.

        Parameters
        ----------
        bounds : `~matplotlib.transforms.Bbox`
        """
        self.dataLim.set(mtransforms.Bbox.union([self.dataLim, bounds]))
