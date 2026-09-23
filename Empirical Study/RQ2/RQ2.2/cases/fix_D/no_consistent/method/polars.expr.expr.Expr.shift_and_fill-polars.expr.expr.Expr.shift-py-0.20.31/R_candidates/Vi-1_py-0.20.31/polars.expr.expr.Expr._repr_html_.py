    def _repr_html_(self) -> str:
        return self._pyexpr.to_str()
