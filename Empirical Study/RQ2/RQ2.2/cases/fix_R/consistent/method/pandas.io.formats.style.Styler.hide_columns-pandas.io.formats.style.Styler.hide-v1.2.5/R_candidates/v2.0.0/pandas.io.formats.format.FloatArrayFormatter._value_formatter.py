    def _value_formatter(
        self,
        float_format: FloatFormatType | None = None,
        threshold: float | None = None,
    ) -> Callable:
        """Returns a function to be applied on each value to format it"""
        # the float_format parameter supersedes self.float_format
        if float_format is None:
            float_format = self.float_format

        # we are going to compose different functions, to first convert to
        # a string, then replace the decimal symbol, and finally chop according
        # to the threshold

        # when there is no float_format, we use str instead of '%g'
        # because str(0.0) = '0.0' while '%g' % 0.0 = '0'
        if float_format:

            def base_formatter(v):
                assert float_format is not None  # for mypy
                # error: "str" not callable
                # error: Unexpected keyword argument "value" for "__call__" of
                # "EngFormatter"
                return (
                    float_format(value=v)  # type: ignore[operator,call-arg]
                    if notna(v)
                    else self.na_rep
                )

        else:

            def base_formatter(v):
                return str(v) if notna(v) else self.na_rep

        if self.decimal != ".":

            def decimal_formatter(v):
                return base_formatter(v).replace(".", self.decimal, 1)

        else:
            decimal_formatter = base_formatter

        if threshold is None:
            return decimal_formatter

        def formatter(value):
            if notna(value):
                if abs(value) > threshold:
                    return decimal_formatter(value)
                else:
                    return decimal_formatter(0.0)
            else:
                return self.na_rep

        return formatter
