    def transform_non_affine(self, a):
        with np.errstate(invalid="ignore"):
            a = np.where(a <= 0, self._fill_value, a)
        return np.divide(np.log(a, out=a), np.log(self.base), out=a)
