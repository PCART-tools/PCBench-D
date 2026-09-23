    def _get_value(self, label, takeable=False):
        if takeable is True:
            return com._maybe_box_datetimelike(self._values[label])
        return self.index.get_value(self._values, label)
