    def is_floating(self) -> bool:
        return self.inferred_type in ["floating", "mixed-integer-float", "integer-na"]
