    @_api.deprecated("3.4", alternative="ax.get_subplotspec().is_first_row()")
    def is_first_row(self):
        return self.get_subplotspec().rowspan.start == 0
