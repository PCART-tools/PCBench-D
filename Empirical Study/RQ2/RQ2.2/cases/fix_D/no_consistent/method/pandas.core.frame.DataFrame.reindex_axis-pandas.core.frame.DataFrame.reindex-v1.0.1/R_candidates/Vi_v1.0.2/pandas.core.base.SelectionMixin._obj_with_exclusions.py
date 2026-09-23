    @cache_readonly
    def _obj_with_exclusions(self):
        if self._selection is not None and isinstance(self.obj, ABCDataFrame):
            return self.obj.reindex(columns=self._selection_list)

        if len(self.exclusions) > 0:
            return self.obj.drop(self.exclusions, axis=1)
        else:
            return self.obj
