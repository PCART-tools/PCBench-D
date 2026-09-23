    def _format_strings(self) -> list[str]:
        values = extract_array(self.values, extract_numpy=True)

        formatter = self.formatter
        if formatter is None:
            # error: Item "ndarray" of "Union[Any, Union[ExtensionArray, ndarray]]" has
            # no attribute "_formatter"
            formatter = values._formatter(boxed=True)  # type: ignore[union-attr]

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
        )
        return fmt_values
