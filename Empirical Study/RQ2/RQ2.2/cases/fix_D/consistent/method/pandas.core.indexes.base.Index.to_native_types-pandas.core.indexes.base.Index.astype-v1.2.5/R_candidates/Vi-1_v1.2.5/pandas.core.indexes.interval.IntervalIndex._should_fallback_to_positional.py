    def _should_fallback_to_positional(self) -> bool:
        # integer lookups in Series.__getitem__ are unambiguously
        #  positional in this case
        return self.dtype.subtype.kind in ["m", "M"]
