    def __getitem__(self, key):
        if self._selection is not None:
            raise Exception('Column(s) %s already selected' % self._selection)

        if (isinstance(key, (list, tuple, Series, np.ndarray)) or
                not self.as_index):
            return DataFrameGroupBy(self.obj, self.grouper, selection=key,
                                    grouper=self.grouper,
                                    exclusions=self.exclusions,
                                    as_index=self.as_index)
        else:
            if key not in self.obj:  # pragma: no cover
                raise KeyError(str(key))
            # kind of a kludge
            return SeriesGroupBy(self.obj[key], selection=key,
                                 grouper=self.grouper,
                                 exclusions=self.exclusions)
