    def _box_func(self, i: int):
        if i == -1:
            return np.nan
        return self.categories[i]
