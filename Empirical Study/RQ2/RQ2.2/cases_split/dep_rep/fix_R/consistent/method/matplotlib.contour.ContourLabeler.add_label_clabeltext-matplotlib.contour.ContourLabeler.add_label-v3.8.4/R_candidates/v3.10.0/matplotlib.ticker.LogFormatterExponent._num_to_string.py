    def _num_to_string(self, x, vmin, vmax):
        fx = math.log(x) / math.log(self._base)
        if 1 <= abs(fx) <= 10000:
            fd = math.log(vmax - vmin) / math.log(self._base)
            s = self._pprint_val(fx, fd)
        else:
            s = f"{fx:1.0g}"
        return s
