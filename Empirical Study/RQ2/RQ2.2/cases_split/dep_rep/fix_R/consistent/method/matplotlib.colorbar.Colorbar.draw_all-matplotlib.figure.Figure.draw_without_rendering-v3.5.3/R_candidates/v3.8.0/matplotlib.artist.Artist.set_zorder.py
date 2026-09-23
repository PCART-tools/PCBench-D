    def set_zorder(self, level):
        """
        Set the zorder for the artist.  Artists with lower zorder
        values are drawn first.

        Parameters
        ----------
        level : float
        """
        if level is None:
            level = self.__class__.zorder
        if level != self.zorder:
            self.zorder = level
            self.pchanged()
            self.stale = True
