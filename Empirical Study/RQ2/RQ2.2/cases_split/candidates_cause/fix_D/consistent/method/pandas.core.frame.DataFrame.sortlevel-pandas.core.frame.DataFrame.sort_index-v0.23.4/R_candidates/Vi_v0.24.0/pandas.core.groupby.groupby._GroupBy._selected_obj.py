    @cache_readonly
    def _selected_obj(self):

        if self._selection is None or isinstance(self.obj, Series):
            if self._group_selection is not None:
                return self.obj[self._group_selection]
            return self.obj
        else:
            return self.obj[self._selection]
