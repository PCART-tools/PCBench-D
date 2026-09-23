    def update_params(self):
        """Update the subplot position from ``self.figure.subplotpars``."""
        self.figbox, _, _, self.numRows, self.numCols = \
            self.get_subplotspec().get_position(self.figure,
                                                return_all=True)
