    def _make_labels(self):
        if self._labels is None or self._group_index is None:
            labels, uniques = algorithms.factorize(
                self.grouper, sort=self.sort)
            uniques = Index(uniques, name=self.name)
            self._labels = labels
            self._group_index = uniques
