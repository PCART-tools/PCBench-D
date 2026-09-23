    @property
    def env_begin(self) -> str:
        return f"\\begin{{tabular}}{{{self.column_format}}}"
