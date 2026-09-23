    def _repr_footer(self) -> str:
        info = self._repr_categories_info()
        return f"Length: {len(self)}\n{info}"
