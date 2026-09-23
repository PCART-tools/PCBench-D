    def set_capstyle(self, cs):
        """Set the capstyle to be one of ('butt', 'round', 'projecting')."""
        cbook._check_in_list(['butt', 'round', 'projecting'], cs=cs)
        self._capstyle = cs
