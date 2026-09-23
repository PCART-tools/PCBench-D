    def __call__(self, x, pos=None):
        if self._minor and x not in self._labelled:
            return ""
        if x <= 0 or x >= 1:
            return ""
        if _is_close_to_int(2 * x) and round(2 * x) == 1:
            s = self._one_half
        elif x < 0.5 and _is_decade(x, rtol=1e-7):
            exponent = round(math.log10(x))
            s = "10^{%d}" % exponent
        elif x > 0.5 and _is_decade(1 - x, rtol=1e-7):
            exponent = round(math.log10(1 - x))
            s = self._one_minus("10^{%d}" % exponent)
        elif x < 0.1:
            s = self._format_value(x, self.locs)
        elif x > 0.9:
            s = self._one_minus(self._format_value(1-x, 1-self.locs))
        else:
            s = self._format_value(x, self.locs, sci_notation=False)
        return r"$\mathdefault{%s}$" % s
