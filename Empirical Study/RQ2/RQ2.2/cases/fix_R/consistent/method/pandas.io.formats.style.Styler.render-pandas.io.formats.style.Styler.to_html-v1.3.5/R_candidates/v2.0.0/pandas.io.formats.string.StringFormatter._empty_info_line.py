    @property
    def _empty_info_line(self) -> str:
        return (
            f"Empty {type(self.frame).__name__}\n"
            f"Columns: {pprint_thing(self.frame.columns)}\n"
            f"Index: {pprint_thing(self.frame.index)}"
        )
