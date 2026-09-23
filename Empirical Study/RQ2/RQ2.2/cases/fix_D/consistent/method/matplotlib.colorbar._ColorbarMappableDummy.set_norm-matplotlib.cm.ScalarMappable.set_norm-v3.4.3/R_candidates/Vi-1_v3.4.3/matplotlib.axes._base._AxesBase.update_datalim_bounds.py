    @_api.deprecated(
        "3.3", alternative="ax.dataLim.set(Bbox.union([ax.dataLim, bounds]))")
    def update_datalim_bounds(self, bounds):
        """
        Extend the `~.Axes.datalim` Bbox to include the given
        `~matplotlib.transforms.Bbox`.

        Parameters
        ----------
        bounds : `~matplotlib.transforms.Bbox`
        """
        self.dataLim.set(mtransforms.Bbox.union([self.dataLim, bounds]))
