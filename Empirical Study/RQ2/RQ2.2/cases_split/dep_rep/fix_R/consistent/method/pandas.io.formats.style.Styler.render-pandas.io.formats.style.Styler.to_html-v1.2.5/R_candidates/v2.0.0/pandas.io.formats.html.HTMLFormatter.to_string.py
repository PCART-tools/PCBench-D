    def to_string(self) -> str:
        lines = self.render()
        if any(isinstance(x, str) for x in lines):
            lines = [str(x) for x in lines]
        return "\n".join(lines)
