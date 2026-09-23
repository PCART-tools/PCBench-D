    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")
        val = np.ma.asarray(value)
        val = val * (self._upper - self._lower) + self._lower
        return self._inv_transform(val)
