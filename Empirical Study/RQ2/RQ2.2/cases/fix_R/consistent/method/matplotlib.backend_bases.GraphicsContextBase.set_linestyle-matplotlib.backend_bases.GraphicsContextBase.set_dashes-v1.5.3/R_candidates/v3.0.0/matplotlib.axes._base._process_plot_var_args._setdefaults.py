    def _setdefaults(self, defaults, *kwargs):
        """
        Given a defaults dictionary, and any other dictionaries,
        update those other dictionaries with information in defaults if
        none of the other dictionaries contains that information.

        """
        for k in defaults:
            if all(kw.get(k, None) is None for kw in kwargs):
                for kw in kwargs:
                    kw[k] = defaults[k]
