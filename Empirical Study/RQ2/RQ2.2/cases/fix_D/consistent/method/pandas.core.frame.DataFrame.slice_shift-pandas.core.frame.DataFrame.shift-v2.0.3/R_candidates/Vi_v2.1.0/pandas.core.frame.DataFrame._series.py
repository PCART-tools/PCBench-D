    @property
    def _series(self):
        return {
            item: Series(
                self._mgr.iget(idx), index=self.index, name=item, fastpath=True
            )
            for idx, item in enumerate(self.columns)
        }
