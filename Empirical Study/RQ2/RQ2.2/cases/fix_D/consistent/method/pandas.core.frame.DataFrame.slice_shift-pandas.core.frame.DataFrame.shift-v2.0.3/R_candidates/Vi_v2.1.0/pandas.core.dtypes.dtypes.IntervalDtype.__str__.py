    def __str__(self) -> str_type:
        if self.subtype is None:
            return "interval"
        if self.closed is None:
            # Only partially initialized GH#38394
            return f"interval[{self.subtype}]"
        return f"interval[{self.subtype}, {self.closed}]"
