    def _format_with_header(
        self, header: list[str], na_rep: str = "NaT", date_format: str | None = None
    ) -> list[str]:
        return header + list(
            self._format_native_types(na_rep=na_rep, date_format=date_format)
        )
