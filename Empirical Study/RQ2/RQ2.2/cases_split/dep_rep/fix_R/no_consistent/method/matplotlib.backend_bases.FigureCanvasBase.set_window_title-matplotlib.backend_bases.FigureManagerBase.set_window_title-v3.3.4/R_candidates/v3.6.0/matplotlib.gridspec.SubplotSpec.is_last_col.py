    def is_last_col(self):
        return self.colspan.stop == self.get_gridspec().ncols
