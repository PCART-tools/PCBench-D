    def set_capstyle(self, cs):
        """Set the capstyle to be one of ('butt', 'round', 'projecting')."""
        if cs in ('butt', 'round', 'projecting'):
            self._capstyle = cs
        else:
            raise ValueError('Unrecognized cap style.  Found %s' % cs)
