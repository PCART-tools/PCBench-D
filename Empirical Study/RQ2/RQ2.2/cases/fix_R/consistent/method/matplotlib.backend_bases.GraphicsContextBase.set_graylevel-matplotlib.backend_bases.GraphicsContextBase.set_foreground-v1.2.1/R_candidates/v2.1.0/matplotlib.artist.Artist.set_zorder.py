    def set_zorder(self, level):
        """
        Set the zorder for the artist.  Artists with lower zorder
        values are drawn first.

        ACCEPTS: any number
        """
        self.zorder = level
        self.pchanged()
        self.stale = True
