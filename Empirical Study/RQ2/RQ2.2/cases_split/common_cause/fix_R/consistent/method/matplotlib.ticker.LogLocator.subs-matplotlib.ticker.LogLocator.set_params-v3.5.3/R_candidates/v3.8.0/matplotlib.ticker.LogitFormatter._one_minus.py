    def _one_minus(self, s):
        if self._use_overline:
            return r"\overline{%s}" % s
        else:
            return f"1-{s}"
