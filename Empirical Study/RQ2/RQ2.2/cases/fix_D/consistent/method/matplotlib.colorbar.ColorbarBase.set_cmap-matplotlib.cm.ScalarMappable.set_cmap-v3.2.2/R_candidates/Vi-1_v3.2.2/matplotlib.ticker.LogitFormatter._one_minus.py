    def _one_minus(self, s):
        if self._use_overline:
            return r"\overline{%s}" % s
        else:
            return "1-{}".format(s)
