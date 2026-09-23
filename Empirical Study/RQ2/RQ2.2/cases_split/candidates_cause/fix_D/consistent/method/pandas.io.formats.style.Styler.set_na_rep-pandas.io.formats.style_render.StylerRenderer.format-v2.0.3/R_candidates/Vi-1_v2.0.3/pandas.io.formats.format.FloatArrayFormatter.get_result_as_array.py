    def get_result_as_array(self) -> np.ndarray:
        """
        Returns the float values converted into strings using
        the parameters given at initialisation, as a numpy array
        """

        def format_with_na_rep(values: ArrayLike, formatter: Callable, na_rep: str):
            mask = isna(values)
            formatted = np.array(
                [
                    formatter(val) if not m else na_rep
                    for val, m in zip(values.ravel(), mask.ravel())
                ]
            ).reshape(values.shape)
            return formatted

        if self.formatter is not None:
            return format_with_na_rep(self.values, self.formatter, self.na_rep)

        if self.fixed_width:
            threshold = get_option("display.chop_threshold")
        else:
            threshold = None

        # if we have a fixed_width, we'll need to try different float_format
        def format_values_with(float_format):
            formatter = self._value_formatter(float_format, threshold)

            # default formatter leaves a space to the left when formatting
            # floats, must be consistent for left-justifying NaNs (GH #25061)
            if self.justify == "left":
                na_rep = " " + self.na_rep
            else:
                na_rep = self.na_rep

            # separate the wheat from the chaff
            values = self.values
            is_complex = is_complex_dtype(values)
            values = format_with_na_rep(values, formatter, na_rep)

            if self.fixed_width:
                if is_complex:
                    result = _trim_zeros_complex(values, self.decimal)
                else:
                    result = _trim_zeros_float(values, self.decimal)
                return np.asarray(result, dtype="object")

            return values

        # There is a special default string when we are fixed-width
        # The default is otherwise to use str instead of a formatting string
        float_format: FloatFormatType | None
        if self.float_format is None:
            if self.fixed_width:
                if self.leading_space is True:
                    fmt_str = "{value: .{digits:d}f}"
                else:
                    fmt_str = "{value:.{digits:d}f}"
                float_format = partial(fmt_str.format, digits=self.digits)
            else:
                float_format = self.float_format
        else:
            float_format = lambda value: self.float_format % value

        formatted_values = format_values_with(float_format)

        if not self.fixed_width:
            return formatted_values

        # we need do convert to engineering format if some values are too small
        # and would appear as 0, or if some values are too big and take too
        # much space

        if len(formatted_values) > 0:
            maxlen = max(len(x) for x in formatted_values)
            too_long = maxlen > self.digits + 6
        else:
            too_long = False

        with np.errstate(invalid="ignore"):
            abs_vals = np.abs(self.values)
            # this is pretty arbitrary for now
            # large values: more that 8 characters including decimal symbol
            # and first digit, hence > 1e6
            has_large_values = (abs_vals > 1e6).any()
            has_small_values = (
                (abs_vals < 10 ** (-self.digits)) & (abs_vals > 0)
            ).any()

        if has_small_values or (too_long and has_large_values):
            if self.leading_space is True:
                fmt_str = "{value: .{digits:d}e}"
            else:
                fmt_str = "{value:.{digits:d}e}"
            float_format = partial(fmt_str.format, digits=self.digits)
            formatted_values = format_values_with(float_format)

        return formatted_values
