    @property
    def _constructor_expanddim(self):
        from pandas.core.frame import DataFrame
        return DataFrame
