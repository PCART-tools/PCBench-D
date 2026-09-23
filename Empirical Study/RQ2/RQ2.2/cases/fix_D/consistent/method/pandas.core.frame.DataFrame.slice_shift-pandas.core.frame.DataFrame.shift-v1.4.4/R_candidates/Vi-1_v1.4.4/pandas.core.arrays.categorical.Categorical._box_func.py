    def _box_func(self, i: int):
        if i == -1:
            return np.NaN
        return self.categories[i]
