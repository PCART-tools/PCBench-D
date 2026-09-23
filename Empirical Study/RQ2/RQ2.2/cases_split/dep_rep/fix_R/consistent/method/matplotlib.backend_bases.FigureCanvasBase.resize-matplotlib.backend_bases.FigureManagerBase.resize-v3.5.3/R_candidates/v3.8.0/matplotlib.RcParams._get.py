    def _get(self, key):
        """
        Directly read data bypassing deprecation, backend and validation
        logic.

        Notes
        -----
        As end user or downstream library you almost always should use
        ``val = rcParams[key]`` and not ``_get()``.

        There are only very few special cases that need direct data access.
        These cases previously used ``dict.__getitem__(rcParams, key, val)``,
        which is now deprecated and replaced by ``rcParams._get(key)``.

        Even though private, we guarantee API stability for ``rcParams._get``,
        i.e. it is subject to Matplotlib's API and deprecation policy.

        :meta public:
        """
        return dict.__getitem__(self, key)
