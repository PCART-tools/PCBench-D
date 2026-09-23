    def _internal_get_values(self):
        # if we are a datetime and period index, return Index to keep metadata
        if is_datetimelike(self.categories):
            return self.categories.take(self._codes, fill_value=np.nan)
        elif is_integer_dtype(self.categories) and -1 in self._codes:
            return self.categories.astype("object").take(self._codes, fill_value=np.nan)
        return np.array(self)
