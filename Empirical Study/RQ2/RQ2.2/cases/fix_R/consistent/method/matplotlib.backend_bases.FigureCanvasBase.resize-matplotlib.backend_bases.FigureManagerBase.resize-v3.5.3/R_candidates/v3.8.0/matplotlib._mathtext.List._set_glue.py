    def _set_glue(self, x: float, sign: int, totals: list[float],
                  error_type: str) -> None:
        self.glue_order = o = next(
            # Highest order of glue used by the members of this list.
            (i for i in range(len(totals))[::-1] if totals[i] != 0), 0)
        self.glue_sign = sign
        if totals[o] != 0.:
            self.glue_set = x / totals[o]
        else:
            self.glue_sign = 0
            self.glue_ratio = 0.
        if o == 0:
            if len(self.children):
                _log.warning("%s %s: %r",
                             error_type, type(self).__name__, self)
