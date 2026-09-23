    def is_numeric(self) -> bool:
        return self.inferred_type in ["integer", "floating"]
