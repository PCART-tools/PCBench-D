    def _format_space(self) -> str:
        space = " " * (len(type(self).__name__) + 1)
        return f"\n{space}"
