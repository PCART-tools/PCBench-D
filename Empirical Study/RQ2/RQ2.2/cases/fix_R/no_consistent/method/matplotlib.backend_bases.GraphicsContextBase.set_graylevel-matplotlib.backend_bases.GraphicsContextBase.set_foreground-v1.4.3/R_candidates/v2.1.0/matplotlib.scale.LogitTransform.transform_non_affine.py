    def transform_non_affine(self, a):
        """logit transform (base 10), masked or clipped"""
        with np.errstate(invalid="ignore"):
            a = np.select(
                [a <= 0, a >= 1], [self._fill_value, 1 - self._fill_value], a)
        return np.log10(a / (1 - a))
