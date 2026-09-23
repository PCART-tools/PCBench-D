    def _num_to_string(self, x, vmin, vmax):
        return self._pprint_val(x, vmax - vmin) if 1 <= x <= 10000 else f"{x:1.0e}"
