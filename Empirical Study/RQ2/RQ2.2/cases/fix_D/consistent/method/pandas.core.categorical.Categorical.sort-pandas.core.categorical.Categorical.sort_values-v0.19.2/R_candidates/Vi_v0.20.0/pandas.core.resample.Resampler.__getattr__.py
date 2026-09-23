    def __getattr__(self, attr):
        if attr in self._internal_names_set:
            return object.__getattribute__(self, attr)
        if attr in self._attributes:
            return getattr(self.groupby, attr)
        if attr in self.obj:
            return self[attr]

        if attr in self._deprecated_invalids:
            raise ValueError(".resample() is now a deferred operation\n"
                             "\tuse .resample(...).mean() instead of "
                             ".resample(...)")

        matches_pattern = any(attr.startswith(x) for x
                              in self._deprecated_valid_patterns)
        if not matches_pattern and attr not in self._deprecated_valids:
            self = self._deprecated(attr)

        return object.__getattribute__(self, attr)
