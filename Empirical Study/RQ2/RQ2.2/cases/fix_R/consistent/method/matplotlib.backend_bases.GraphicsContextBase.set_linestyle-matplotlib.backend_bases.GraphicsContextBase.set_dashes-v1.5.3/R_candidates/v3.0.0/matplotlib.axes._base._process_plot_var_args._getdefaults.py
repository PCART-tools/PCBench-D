    def _getdefaults(self, ignore, *kwargs):
        """
        Only advance the cycler if the cycler has information that
        is not specified in any of the supplied tuple of dicts.
        Ignore any keys specified in the `ignore` set.

        Returns a copy of defaults dictionary if there are any
        keys that are not found in any of the supplied dictionaries.
        If the supplied dictionaries have non-None values for
        everything the property cycler has, then just return
        an empty dictionary. Ignored keys are excluded from the
        returned dictionary.

        """
        prop_keys = self._prop_keys
        if ignore is None:
            ignore = set()
        prop_keys = prop_keys - ignore

        if any(all(kw.get(k, None) is None for kw in kwargs)
               for k in prop_keys):
            # Need to copy this dictionary or else the next time around
            # in the cycle, the dictionary could be missing entries.
            default_dict = next(self.prop_cycler).copy()
            for p in ignore:
                default_dict.pop(p, None)
        else:
            default_dict = {}
        return default_dict
