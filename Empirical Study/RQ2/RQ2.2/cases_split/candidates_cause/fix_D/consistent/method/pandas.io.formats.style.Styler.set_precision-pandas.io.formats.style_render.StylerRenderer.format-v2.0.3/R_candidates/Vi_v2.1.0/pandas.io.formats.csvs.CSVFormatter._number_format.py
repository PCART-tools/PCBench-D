    @property
    def _number_format(self) -> dict[str, Any]:
        """Dictionary used for storing number formatting settings."""
        return {
            "na_rep": self.na_rep,
            "float_format": self.float_format,
            "date_format": self.date_format,
            "quoting": self.quoting,
            "decimal": self.decimal,
        }
