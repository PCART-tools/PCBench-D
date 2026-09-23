    @deprecate_renamed_function("to_integer", version="0.19.14")
    @deprecate_renamed_parameter("radix", "base", version="0.19.14")
    def parse_int(self, base: int | None = None, *, strict: bool = True) -> Expr:
        """
        Parse integers with base radix from strings.

        ParseError/Overflows become Nulls.

        .. deprecated:: 0.19.14
            This method has been renamed to :func:`to_integer`.

        Parameters
        ----------
        base
            Positive integer which is the base of the string we are parsing.
        strict
            Bool, Default=True will raise any ParseError or overflow as ComputeError.
            False silently convert to Null.

        """
        if base is None:
            base = 2
        return self.to_integer(base=base, strict=strict).cast(Int32, strict=strict)
