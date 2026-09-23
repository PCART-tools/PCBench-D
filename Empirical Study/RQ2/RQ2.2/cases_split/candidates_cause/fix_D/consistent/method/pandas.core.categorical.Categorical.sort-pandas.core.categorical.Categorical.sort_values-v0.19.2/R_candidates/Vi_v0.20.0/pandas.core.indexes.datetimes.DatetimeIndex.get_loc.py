    def get_loc(self, key, method=None, tolerance=None):
        """
        Get integer location for requested label

        Returns
        -------
        loc : int
        """

        if tolerance is not None:
            # try converting tolerance now, so errors don't get swallowed by
            # the try/except clauses below
            tolerance = self._convert_tolerance(tolerance)

        if isinstance(key, datetime):
            # needed to localize naive datetimes
            key = Timestamp(key, tz=self.tz)
            return Index.get_loc(self, key, method, tolerance)

        if isinstance(key, time):
            if method is not None:
                raise NotImplementedError('cannot yet lookup inexact labels '
                                          'when key is a time object')
            return self.indexer_at_time(key)

        try:
            return Index.get_loc(self, key, method, tolerance)
        except (KeyError, ValueError, TypeError):
            try:
                return self._get_string_slice(key)
            except (TypeError, KeyError, ValueError):
                pass

            try:
                stamp = Timestamp(key, tz=self.tz)
                return Index.get_loc(self, stamp, method, tolerance)
            except (KeyError, ValueError):
                raise KeyError(key)
