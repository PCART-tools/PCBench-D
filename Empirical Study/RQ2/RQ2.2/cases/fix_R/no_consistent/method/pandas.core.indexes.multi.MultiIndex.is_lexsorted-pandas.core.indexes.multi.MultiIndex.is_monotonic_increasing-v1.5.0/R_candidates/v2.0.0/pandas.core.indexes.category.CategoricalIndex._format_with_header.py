    def _format_with_header(self, header: list[str], na_rep: str) -> list[str]:
        result = [
            pprint_thing(x, escape_chars=("\t", "\r", "\n")) if notna(x) else na_rep
            for x in self._values
        ]
        return header + result
