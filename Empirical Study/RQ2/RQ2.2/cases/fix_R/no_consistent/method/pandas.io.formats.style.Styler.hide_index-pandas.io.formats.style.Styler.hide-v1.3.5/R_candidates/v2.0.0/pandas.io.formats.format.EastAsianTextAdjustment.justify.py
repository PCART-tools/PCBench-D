    def justify(
        self, texts: Iterable[str], max_len: int, mode: str = "right"
    ) -> list[str]:
        # re-calculate padding space per str considering East Asian Width
        def _get_pad(t):
            return max_len - self.len(t) + len(t)

        if mode == "left":
            return [x.ljust(_get_pad(x)) for x in texts]
        elif mode == "center":
            return [x.center(_get_pad(x)) for x in texts]
        else:
            return [x.rjust(_get_pad(x)) for x in texts]
