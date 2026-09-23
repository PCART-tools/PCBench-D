    def _format_with_header(self, header: list[str], na_rep: str) -> list[str]:
        # matches base class except for whitespace padding
        return header + list(self._format_native_types(na_rep=na_rep))
