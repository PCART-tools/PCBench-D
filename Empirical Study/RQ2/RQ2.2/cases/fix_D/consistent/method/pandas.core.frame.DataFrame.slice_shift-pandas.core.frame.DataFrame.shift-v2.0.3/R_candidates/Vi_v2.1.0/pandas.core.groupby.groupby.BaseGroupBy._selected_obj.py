    @final
    @cache_readonly
    def _selected_obj(self):
        # Note: _selected_obj is always just `self.obj` for SeriesGroupBy
        if isinstance(self.obj, Series):
            return self.obj

        if self._selection is not None:
            if is_hashable(self._selection):
                # i.e. a single key, so selecting it will return a Series.
                #  In this case, _obj_with_exclusions would wrap the key
                #  in a list and return a single-column DataFrame.
                return self.obj[self._selection]

            # Otherwise _selection is equivalent to _selection_list, so
            #  _selected_obj matches _obj_with_exclusions, so we can re-use
            #  that and avoid making a copy.
            return self._obj_with_exclusions

        return self.obj
