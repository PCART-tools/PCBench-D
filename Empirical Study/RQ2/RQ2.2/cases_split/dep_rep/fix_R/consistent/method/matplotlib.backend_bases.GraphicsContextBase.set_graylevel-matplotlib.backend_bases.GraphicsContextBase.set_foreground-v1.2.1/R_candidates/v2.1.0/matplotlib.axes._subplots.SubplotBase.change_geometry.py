    def change_geometry(self, numrows, numcols, num):
        """change subplot geometry, e.g., from 1,1,1 to 2,2,3"""
        self._subplotspec = GridSpec(numrows, numcols)[num - 1]
        self.update_params()
        self.set_position(self.figbox)
