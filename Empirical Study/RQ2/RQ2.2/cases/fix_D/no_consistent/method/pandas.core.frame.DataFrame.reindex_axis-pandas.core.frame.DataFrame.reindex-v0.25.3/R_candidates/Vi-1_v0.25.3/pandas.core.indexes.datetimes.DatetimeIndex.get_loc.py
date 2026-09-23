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
            tolerance = self._convert_tolerance(tolerance, np.asarray(key))

        if isinstance(key, datetime):
            # needed to localize naive datetimes
            if key.tzinfo is None:
                key = Timestamp(key, tz=self.tz)
            else:
                key = Timestamp(key).tz_convert(self.tz)
            return Index.get_loc(self, key, method, tolerance)

        elif isinstance(key, timedelta):
            # GH#20464
            raise TypeError(
                "Cannot index {cls} with {other}".format(
                    cls=type(self).__name__, other=type(key).__name__
                )
            )

        if isinstance(key, time):
            if method is not None:
                raise NotImplementedError(
                    "cannot yet lookup inexact labels " "when key is a time object"
                )
            return self.indexer_at_time(key)

        try:
            return Index.get_loc(self, key, method, tolerance)
        except (KeyError, ValueError, TypeError):
            try:
                return self._get_string_slice(key)
            except (TypeError, KeyError, ValueError, OverflowError):
                pass

            try:
                stamp = Timestamp(key)
                if stamp.tzinfo is not None and self.tz is not None:
                    stamp = stamp.tz_convert(self.tz)
                else:
                    stamp = stamp.tz_localize(self.tz)
                return Index.get_loc(self, stamp, method, tolerance)
            except KeyError:
                raise KeyError(key)
            except ValueError as e:
                # list-like tolerance size must match target index size
                if "list-like" in str(e):
                    raise e
                raise KeyError(key)
