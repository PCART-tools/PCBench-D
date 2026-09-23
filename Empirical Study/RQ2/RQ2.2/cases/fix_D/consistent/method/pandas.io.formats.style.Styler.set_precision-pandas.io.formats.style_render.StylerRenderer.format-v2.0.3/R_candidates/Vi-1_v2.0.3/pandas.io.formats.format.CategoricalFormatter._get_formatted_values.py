    def _get_formatted_values(self) -> list[str]:
        return format_array(
            self.categorical._internal_get_values(),
            None,
            float_format=None,
            na_rep=self.na_rep,
            quoting=self.quoting,
        )
