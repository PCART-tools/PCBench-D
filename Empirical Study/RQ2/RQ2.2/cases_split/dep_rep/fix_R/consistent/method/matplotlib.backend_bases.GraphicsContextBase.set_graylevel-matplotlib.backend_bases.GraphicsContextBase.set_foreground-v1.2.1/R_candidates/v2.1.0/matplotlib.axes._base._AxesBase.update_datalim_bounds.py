    def update_datalim_bounds(self, bounds):
        """
        Update the datalim to include the given
        :class:`~matplotlib.transforms.Bbox` *bounds*
        """
        self.dataLim.set(mtransforms.Bbox.union([self.dataLim, bounds]))
