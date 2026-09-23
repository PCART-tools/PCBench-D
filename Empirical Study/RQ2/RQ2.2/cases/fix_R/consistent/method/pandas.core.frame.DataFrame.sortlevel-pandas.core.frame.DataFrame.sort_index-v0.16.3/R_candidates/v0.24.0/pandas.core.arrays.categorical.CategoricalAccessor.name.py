    @property
    def name(self):
        # Note: Upon deprecation, `test_tab_completion_with_categorical` will
        # need to be updated. `name` will need to be removed from
        # `ok_for_cat`.
        warn("`Series.cat.name` has been deprecated. Use `Series.name` "
             "instead.",
             FutureWarning,
             stacklevel=2)
        return self._name
