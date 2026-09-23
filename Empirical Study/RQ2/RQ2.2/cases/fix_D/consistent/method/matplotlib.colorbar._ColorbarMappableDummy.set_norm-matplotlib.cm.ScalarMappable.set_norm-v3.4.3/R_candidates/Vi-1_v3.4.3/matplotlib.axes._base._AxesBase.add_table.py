    def add_table(self, tab):
        """
        Add a `~.Table` to the axes' tables; return the table.
        """
        self._set_artist_props(tab)
        self.tables.append(tab)
        tab.set_clip_path(self.patch)
        tab._remove_method = self.tables.remove
        return tab
