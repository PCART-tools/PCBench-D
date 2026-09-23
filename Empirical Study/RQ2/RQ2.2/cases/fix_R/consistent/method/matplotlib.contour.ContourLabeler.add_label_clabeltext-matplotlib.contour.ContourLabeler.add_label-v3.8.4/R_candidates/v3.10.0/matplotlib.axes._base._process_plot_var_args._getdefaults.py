    def _getdefaults(self, kw, ignore=frozenset()):
        """
        If some keys in the property cycle (excluding those in the set
        *ignore*) are absent or set to None in the dict *kw*, return a copy
        of the next entry in the property cycle, excluding keys in *ignore*.
        Otherwise, don't advance the property cycle, and return an empty dict.
        """
        defaults = self._cycler_items[self._idx]
        if any(kw.get(k, None) is None for k in {*defaults} - ignore):
            self._idx = (self._idx + 1) % len(self._cycler_items)  # Advance cycler.
            # Return a new dict to avoid exposing _cycler_items entries to mutation.
            return {k: v for k, v in defaults.items() if k not in ignore}
        else:
            return {}
