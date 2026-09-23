    @_api.deprecated("3.4", alternative="get_gridspec().nrows")
    @property
    def numRows(self):
        return self.get_gridspec().nrows
