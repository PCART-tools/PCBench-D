    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int
        """
        if is_list_like(key):
            raise TypeError

        if isna(key):
            key = NaT

        if tolerance is not None:
            # try converting tolerance now, so errors don't get swallowed by
            # the try/except clauses below
            tolerance = self._convert_tolerance(tolerance, np.asarray(key))

        if _is_convertible_to_td(key):
            key = Timedelta(key)
            return Index.get_loc(self, key, method, tolerance)

        try:
            return Index.get_loc(self, key, method, tolerance)
        except (KeyError, ValueError, TypeError):
            try:
                return self._get_string_slice(key)
            except (TypeError, KeyError, ValueError):
                pass

            try:
                stamp = Timedelta(key)
                return Index.get_loc(self, stamp, method, tolerance)
            except (KeyError, ValueError):
                raise KeyError(key)
