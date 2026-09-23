    def _format_with_header(self, header: List[str], na_rep: str = "NaN") -> List[str]:
        return header + list(self._format_native_types(na_rep=na_rep))
