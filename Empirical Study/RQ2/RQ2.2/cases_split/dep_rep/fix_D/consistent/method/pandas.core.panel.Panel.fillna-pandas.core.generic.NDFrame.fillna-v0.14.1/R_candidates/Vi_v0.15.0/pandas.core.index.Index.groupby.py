    def groupby(self, to_groupby):
        return self._groupby(self.values, _values_from_object(to_groupby))
