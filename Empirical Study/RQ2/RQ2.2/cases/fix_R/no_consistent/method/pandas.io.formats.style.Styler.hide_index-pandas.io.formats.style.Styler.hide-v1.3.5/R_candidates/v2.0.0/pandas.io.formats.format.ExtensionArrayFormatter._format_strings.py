    def _format_strings(self) -> list[str]:
        values = extract_array(self.values, extract_numpy=True)

        formatter = self.formatter
        fallback_formatter = None
        if formatter is None:
            fallback_formatter = values._formatter(boxed=True)

        if isinstance(values, Categorical):
            # Categorical is special for now, so that we can preserve tzinfo
            array = values._internal_get_values()
        else:
            array = np.asarray(values)

        fmt_values = format_array(
            array,
            formatter,
            float_format=self.float_format,
            na_rep=self.na_rep,
            digits=self.digits,
            space=self.space,
            justify=self.justify,
            decimal=self.decimal,
            leading_space=self.leading_space,
            quoting=self.quoting,
            fallback_formatter=fallback_formatter,
        )
        return fmt_values
