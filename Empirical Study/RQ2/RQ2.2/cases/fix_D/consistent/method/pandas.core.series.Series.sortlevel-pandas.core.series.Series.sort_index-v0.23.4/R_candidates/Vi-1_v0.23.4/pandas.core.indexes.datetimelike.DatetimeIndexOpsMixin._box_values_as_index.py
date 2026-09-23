    def _box_values_as_index(self):
        """
        return object Index which contains boxed values
        """
        from pandas.core.index import Index
        return Index(self._box_values(self.asi8), name=self.name, dtype=object)
