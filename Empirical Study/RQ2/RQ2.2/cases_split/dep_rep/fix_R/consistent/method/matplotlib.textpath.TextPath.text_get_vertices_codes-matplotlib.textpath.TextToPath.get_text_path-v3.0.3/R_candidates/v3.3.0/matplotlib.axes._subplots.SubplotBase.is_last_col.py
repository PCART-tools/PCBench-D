    def is_last_col(self):
        return self.get_subplotspec().colspan.stop == self.get_gridspec().ncols
