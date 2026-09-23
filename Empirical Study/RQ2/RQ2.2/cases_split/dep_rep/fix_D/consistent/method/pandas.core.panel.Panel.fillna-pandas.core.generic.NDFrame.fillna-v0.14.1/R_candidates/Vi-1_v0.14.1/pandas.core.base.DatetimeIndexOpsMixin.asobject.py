    @property
    def asobject(self):
        from pandas.core.index import Index
        return Index(self._box_values(self.asi8), name=self.name, dtype=object)
