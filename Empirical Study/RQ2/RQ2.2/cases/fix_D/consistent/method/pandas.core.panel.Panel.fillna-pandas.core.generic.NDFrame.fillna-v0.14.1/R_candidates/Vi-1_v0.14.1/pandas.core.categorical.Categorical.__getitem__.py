    def __getitem__(self, key):
        if isinstance(key, (int, np.integer)):
            i = self.labels[key]
            if i == -1:
                return np.nan
            else:
                return self.levels[i]
        else:
            return Categorical(self.labels[key], self.levels)
