    def asof(self, label):
        """
        For a sorted index, return the most recent label up to and including
        the passed label. Return NaN if not found.

        See also
        --------
        get_loc : asof is a thin wrapper around get_loc with method='pad'
        """
        try:
            loc = self.get_loc(label, method='pad')
        except KeyError:
            return self._na_value
        else:
            if isinstance(loc, slice):
                loc = loc.indices(len(self))[-1]
            return self[loc]
