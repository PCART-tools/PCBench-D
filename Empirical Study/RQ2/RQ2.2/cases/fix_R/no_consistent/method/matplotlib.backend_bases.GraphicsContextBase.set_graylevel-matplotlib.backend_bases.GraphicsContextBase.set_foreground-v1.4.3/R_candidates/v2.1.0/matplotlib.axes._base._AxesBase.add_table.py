    def add_table(self, tab):
        """
        Add a :class:`~matplotlib.tables.Table` instance to the
        list of axes tables

        Returns the table.
        """
        self._set_artist_props(tab)
        self.tables.append(tab)
        tab.set_clip_path(self.patch)
        tab._remove_method = lambda h: self.tables.remove(h)
        return tab
