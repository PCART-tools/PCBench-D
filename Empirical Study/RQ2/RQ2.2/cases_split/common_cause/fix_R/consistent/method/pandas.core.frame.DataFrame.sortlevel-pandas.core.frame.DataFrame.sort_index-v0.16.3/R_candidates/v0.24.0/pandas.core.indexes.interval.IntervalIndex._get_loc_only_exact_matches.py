    def _get_loc_only_exact_matches(self, key):
        if isinstance(key, Interval):

            if not self.is_unique:
                raise ValueError("cannot index with a slice Interval"
                                 " and a non-unique index")

            # TODO: this expands to a tuple index, see if we can
            # do better
            return Index(self._multiindex.values).get_loc(key)
        raise KeyError
