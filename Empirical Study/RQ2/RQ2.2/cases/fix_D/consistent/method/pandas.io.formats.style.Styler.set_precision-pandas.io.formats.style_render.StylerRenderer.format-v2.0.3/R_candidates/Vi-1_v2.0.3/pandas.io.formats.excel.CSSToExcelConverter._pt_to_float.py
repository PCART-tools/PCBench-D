    def _pt_to_float(self, pt_string: str) -> float:
        assert pt_string.endswith("pt")
        return float(pt_string.rstrip("pt"))
