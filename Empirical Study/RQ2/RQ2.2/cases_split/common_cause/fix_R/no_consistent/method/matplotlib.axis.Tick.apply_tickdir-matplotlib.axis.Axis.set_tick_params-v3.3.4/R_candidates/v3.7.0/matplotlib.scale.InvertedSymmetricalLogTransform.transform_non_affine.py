    def transform_non_affine(self, a):
        abs_a = np.abs(a)
        if (abs_a < self.linthresh).all():
            _api.warn_external(
                "All values for SymLogScale are below linthresh, making "
                "it effectively linear. You likely should lower the value "
                "of linthresh. ")
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.sign(a) * self.linthresh * (
                np.power(self.base,
                         abs_a / self.linthresh - self._linscale_adj))
            inside = abs_a <= self.invlinthresh
        out[inside] = a[inside] / self._linscale_adj
        return out
