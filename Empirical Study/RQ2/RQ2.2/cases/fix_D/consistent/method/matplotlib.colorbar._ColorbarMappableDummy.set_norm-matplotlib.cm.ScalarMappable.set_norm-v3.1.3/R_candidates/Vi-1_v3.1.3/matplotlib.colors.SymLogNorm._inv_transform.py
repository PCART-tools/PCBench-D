    def _inv_transform(self, a):
        """Inverse inplace Transformation."""
        masked = np.abs(a) > (self.linthresh * self._linscale_adj)
        sign = np.sign(a[masked])
        exp = np.exp(sign * a[masked] / self.linthresh - self._linscale_adj)
        exp *= sign * self.linthresh
        a[masked] = exp
        a[~masked] /= self._linscale_adj
        return a
