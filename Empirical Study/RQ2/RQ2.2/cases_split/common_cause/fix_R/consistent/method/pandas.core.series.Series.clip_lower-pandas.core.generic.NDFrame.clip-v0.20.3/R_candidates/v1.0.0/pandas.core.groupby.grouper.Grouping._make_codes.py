    def _make_codes(self) -> None:
        if self._codes is None or self._group_index is None:
            # we have a list of groupers
            if isinstance(self.grouper, ops.BaseGrouper):
                codes = self.grouper.codes_info
                uniques = self.grouper.result_index
            else:
                codes, uniques = algorithms.factorize(self.grouper, sort=self.sort)
                uniques = Index(uniques, name=self.name)
            self._codes = codes
            self._group_index = uniques
