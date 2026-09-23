    @_api.deprecated("3.4", alternative="get_gridspec().ncols")
    @property
    def numCols(self):
        return self.get_gridspec().ncols
