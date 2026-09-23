    def _make_labels(self):
        if self._labels is None or self._group_index is None:
            # we have a list of groupers
            if isinstance(self.grouper, BaseGrouper):
                labels = self.grouper.label_info
                uniques = self.grouper.result_index
            else:
                labels, uniques = algorithms.factorize(self.grouper, sort=self.sort)
                uniques = Index(uniques, name=self.name)
            self._labels = labels
            self._group_index = uniques
