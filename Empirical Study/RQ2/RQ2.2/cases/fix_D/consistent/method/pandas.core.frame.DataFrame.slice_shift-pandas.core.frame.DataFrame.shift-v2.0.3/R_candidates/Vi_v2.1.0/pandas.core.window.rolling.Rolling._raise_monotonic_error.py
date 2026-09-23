    def _raise_monotonic_error(self, msg: str):
        on = self.on
        if on is None:
            if self.axis == 0:
                on = "index"
            else:
                on = "column"
        raise ValueError(f"{on} {msg}")
