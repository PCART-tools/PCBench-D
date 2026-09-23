    def __str__(self) -> str_type:
        if self.subtype is None:
            return "interval"
        return f"interval[{self.subtype}]"
