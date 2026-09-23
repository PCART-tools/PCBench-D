    @_api.deprecated("3.4", alternative="ax.get_subplotspec().is_first_col()")
    def is_first_col(self):
        return self.get_subplotspec().colspan.start == 0
