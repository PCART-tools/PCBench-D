    @cache_readonly
    def _selected_obj(self):

        if self._selection is None or isinstance(self.obj, ABCSeries):
            return self.obj
        else:
            return self.obj[self._selection]
