    def _get_flat_col_name(self, col: str | tuple) -> str:
        flat_col = col
        if isinstance(col, tuple):
            flat_col = (
                "".join([str(c) for c in col]).strip()
                if "" in col
                else "_".join([str(c) for c in col]).strip()
            )
        return f"{self.prefix_uri}{flat_col}"
