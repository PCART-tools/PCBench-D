    @property
    def _constructor_expanddim(self):
        from pandas.core.panel import Panel
        return Panel
