    @_api.deprecated("3.4", alternative="ax.get_subplotspec().is_last_row()")
    def is_last_row(self):
        return self.get_subplotspec().rowspan.stop == self.get_gridspec().nrows
