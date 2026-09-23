    @property
    def _empty_info_line(self):
        return (
            f"Empty {type(self.frame).__name__}\n"
            f"Columns: {self.frame.columns}\n"
            f"Index: {self.frame.index}"
        )
