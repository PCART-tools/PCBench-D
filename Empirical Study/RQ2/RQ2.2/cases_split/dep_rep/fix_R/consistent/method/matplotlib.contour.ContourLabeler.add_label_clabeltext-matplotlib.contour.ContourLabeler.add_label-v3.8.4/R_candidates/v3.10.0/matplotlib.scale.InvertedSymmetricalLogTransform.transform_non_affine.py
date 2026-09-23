    def transform_non_affine(self, values):
        abs_a = np.abs(values)
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.sign(values) * self.linthresh * (
                np.power(self.base,
                         abs_a / self.linthresh - self._linscale_adj))
            inside = abs_a <= self.invlinthresh
        out[inside] = values[inside] / self._linscale_adj
        return out
