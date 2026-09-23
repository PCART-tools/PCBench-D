    def is_last_row(self):
        return self.get_subplotspec().rowspan.stop == self.get_gridspec().nrows
