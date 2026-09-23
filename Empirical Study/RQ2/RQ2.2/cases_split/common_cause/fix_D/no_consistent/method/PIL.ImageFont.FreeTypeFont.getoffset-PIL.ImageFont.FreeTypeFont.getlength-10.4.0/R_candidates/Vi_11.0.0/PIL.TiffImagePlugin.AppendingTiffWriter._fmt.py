    def _fmt(self, field_size: int) -> str:
        try:
            return {2: "H", 4: "L", 8: "Q"}[field_size]
        except KeyError:
            msg = "offset is not supported"
            raise RuntimeError(msg)
