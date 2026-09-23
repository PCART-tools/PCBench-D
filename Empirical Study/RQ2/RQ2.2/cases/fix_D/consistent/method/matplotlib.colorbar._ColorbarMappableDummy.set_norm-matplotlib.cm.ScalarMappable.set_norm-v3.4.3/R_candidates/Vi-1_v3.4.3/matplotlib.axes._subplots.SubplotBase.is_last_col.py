    @_api.deprecated("3.4", alternative="ax.get_subplotspec().is_last_col()")
    def is_last_col(self):
        return self.get_subplotspec().colspan.stop == self.get_gridspec().ncols
