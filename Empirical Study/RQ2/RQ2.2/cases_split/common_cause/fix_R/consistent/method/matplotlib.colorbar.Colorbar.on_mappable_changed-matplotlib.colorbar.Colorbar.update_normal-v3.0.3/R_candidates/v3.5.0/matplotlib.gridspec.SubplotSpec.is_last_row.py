    def is_last_row(self):
        return self.rowspan.stop == self.get_gridspec().nrows
