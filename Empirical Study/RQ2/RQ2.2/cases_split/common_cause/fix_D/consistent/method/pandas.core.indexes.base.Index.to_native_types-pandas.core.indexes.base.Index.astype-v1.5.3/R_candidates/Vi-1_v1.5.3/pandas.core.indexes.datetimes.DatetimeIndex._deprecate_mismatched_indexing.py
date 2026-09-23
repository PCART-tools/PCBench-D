    def _deprecate_mismatched_indexing(self, key, one_way: bool = False) -> None:
        # GH#36148
        # we get here with isinstance(key, self._data._recognized_scalars)
        try:
            self._data._assert_tzawareness_compat(key)
        except TypeError:
            if self.tz is None:
                msg = (
                    "Indexing a timezone-naive DatetimeIndex with a "
                    "timezone-aware datetime is deprecated and will "
                    "raise KeyError in a future version.  "
                    "Use a timezone-naive object instead."
                )
            elif one_way:
                # we special-case timezone-naive strings and timezone-aware
                #  DatetimeIndex
                return
            else:
                msg = (
                    "Indexing a timezone-aware DatetimeIndex with a "
                    "timezone-naive datetime is deprecated and will "
                    "raise KeyError in a future version. "
                    "Use a timezone-aware object instead."
                )
            warnings.warn(msg, FutureWarning, stacklevel=find_stack_level())
