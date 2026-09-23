    def _getdefaults(self, ignore, kw):
        """
        If some keys in the property cycle (excluding those in the set
        *ignore*) are absent or set to None in the dict *kw*, return a copy
        of the next entry in the property cycle, excluding keys in *ignore*.
        Otherwise, don't advance the property cycle, and return an empty dict.
        """
        prop_keys = self._prop_keys - ignore
        if any(kw.get(k, None) is None for k in prop_keys):
            # Need to copy this dictionary or else the next time around
            # in the cycle, the dictionary could be missing entries.
            default_dict = self._cycler_items[self._idx].copy()
            self._idx = (self._idx + 1) % len(self._cycler_items)
            for p in ignore:
                default_dict.pop(p, None)
        else:
            default_dict = {}
        return default_dict
