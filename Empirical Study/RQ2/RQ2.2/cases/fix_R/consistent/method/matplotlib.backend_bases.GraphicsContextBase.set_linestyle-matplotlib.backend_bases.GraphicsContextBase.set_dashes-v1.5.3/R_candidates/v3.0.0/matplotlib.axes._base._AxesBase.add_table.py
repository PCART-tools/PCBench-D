    def add_table(self, tab):
        """
        Add a :class:`~matplotlib.table.Table` instance to the
        list of axes tables

        Parameters
        ----------
        tab: `matplotlib.table.Table`
            Table instance

        Returns
        -------
        `matplotlib.table.Table`: the table.
        """
        self._set_artist_props(tab)
        self.tables.append(tab)
        tab.set_clip_path(self.patch)
        tab._remove_method = self.tables.remove
        return tab
