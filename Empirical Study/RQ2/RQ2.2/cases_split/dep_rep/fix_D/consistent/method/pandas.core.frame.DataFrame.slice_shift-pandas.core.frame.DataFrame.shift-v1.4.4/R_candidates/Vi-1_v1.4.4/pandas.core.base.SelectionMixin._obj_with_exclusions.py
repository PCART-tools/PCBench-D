    @final
    @cache_readonly
    def _obj_with_exclusions(self):
        if self._selection is not None and isinstance(self.obj, ABCDataFrame):
            return self.obj[self._selection_list]

        if len(self.exclusions) > 0:
            # equivalent to `self.obj.drop(self.exclusions, axis=1)
            #  but this avoids consolidating and making a copy
            return self.obj._drop_axis(
                self.exclusions, axis=1, consolidate=False, only_slice=True
            )
        else:
            return self.obj
