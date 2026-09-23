    def _make_labels(self):
        if self._was_factor:  # pragma: no cover
            raise Exception('Should not call this method grouping by level')
        else:
            labels, uniques = algos.factorize(self.grouper, sort=self.sort)
            uniques = Index(uniques, name=self.name)
            self._labels = labels
            self._group_index = uniques
