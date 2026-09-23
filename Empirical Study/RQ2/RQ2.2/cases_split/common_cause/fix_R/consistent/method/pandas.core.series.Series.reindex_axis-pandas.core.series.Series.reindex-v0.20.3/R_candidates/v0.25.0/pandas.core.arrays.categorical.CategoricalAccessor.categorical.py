    @property
    def categorical(self):
        # Note: Upon deprecation, `test_tab_completion_with_categorical` will
        # need to be updated. `categorical` will need to be removed from
        # `ok_for_cat`.
        warn(
            "`Series.cat.categorical` has been deprecated. Use the "
            "attributes on 'Series.cat' directly instead.",
            FutureWarning,
            stacklevel=2,
        )
        return self._parent
