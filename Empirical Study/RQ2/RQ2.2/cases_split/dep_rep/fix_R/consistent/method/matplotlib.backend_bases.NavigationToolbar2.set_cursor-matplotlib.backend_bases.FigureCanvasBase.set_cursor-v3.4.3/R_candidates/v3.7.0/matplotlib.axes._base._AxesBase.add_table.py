    def add_table(self, tab):
        """
        Add a `.Table` to the Axes; return the table.
        """
        _api.check_isinstance(mtable.Table, tab=tab)
        self._set_artist_props(tab)
        self._children.append(tab)
        tab.set_clip_path(self.patch)
        tab._remove_method = self._children.remove
        return tab
