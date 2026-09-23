    def _set(self, key, val):
        """
        Directly write data bypassing deprecation and validation logic.

        Notes
        -----
        As end user or downstream library you almost always should use
        ``rcParams[key] = val`` and not ``_set()``.

        There are only very few special cases that need direct data access.
        These cases previously used ``dict.__setitem__(rcParams, key, val)``,
        which is now deprecated and replaced by ``rcParams._set(key, val)``.

        Even though private, we guarantee API stability for ``rcParams._set``,
        i.e. it is subject to Matplotlib's API and deprecation policy.

        :meta public:
        """
        dict.__setitem__(self, key, val)
