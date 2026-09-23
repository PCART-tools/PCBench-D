    def _get_value(self, label, takeable=False):
        loc = label if takeable is True else self.index.get_loc(label)
        return self._get_val_at(loc)
