    def __getitem__(self, key):
        if self._selection is not None:
            raise Exception('Column(s) %s already selected' % self._selection)

        if isinstance(key, (list, tuple, Series, Index, np.ndarray)):
            if len(self.obj.columns.intersection(key)) != len(key):
                bad_keys = list(set(key).difference(self.obj.columns))
                raise KeyError("Columns not found: %s"
                               % str(bad_keys)[1:-1])
            return DataFrameGroupBy(self.obj, self.grouper, selection=key,
                                    grouper=self.grouper,
                                    exclusions=self.exclusions,
                                    as_index=self.as_index)

        elif not self.as_index:
            if key not in self.obj.columns:
                raise KeyError("Column not found: %s" % key)
            return DataFrameGroupBy(self.obj, self.grouper, selection=key,
                                    grouper=self.grouper,
                                    exclusions=self.exclusions,
                                    as_index=self.as_index)

        else:
            if key not in self.obj:
                raise KeyError("Column not found: %s" % key)
            # kind of a kludge
            return SeriesGroupBy(self.obj[key], selection=key,
                                 grouper=self.grouper,
                                 exclusions=self.exclusions)
