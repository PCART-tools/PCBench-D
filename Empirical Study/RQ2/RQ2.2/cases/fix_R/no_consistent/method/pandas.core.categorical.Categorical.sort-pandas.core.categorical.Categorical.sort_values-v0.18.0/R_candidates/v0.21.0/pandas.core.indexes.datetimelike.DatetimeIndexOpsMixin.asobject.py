    @property
    def asobject(self):
        """
        return object Index which contains boxed values

        *this is an internal non-public method*
        """
        from pandas.core.index import Index
        return Index(self._box_values(self.asi8), name=self.name, dtype=object)
