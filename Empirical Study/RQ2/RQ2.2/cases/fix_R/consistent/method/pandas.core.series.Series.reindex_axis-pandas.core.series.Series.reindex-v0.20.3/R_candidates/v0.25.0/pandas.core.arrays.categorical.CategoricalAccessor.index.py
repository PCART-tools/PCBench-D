    @property
    def index(self):
        # Note: Upon deprecation, `test_tab_completion_with_categorical` will
        # need to be updated. `index` will need to be removed from
        # ok_for_cat`.
        warn(
            "`Series.cat.index` has been deprecated. Use `Series.index` " "instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._index
