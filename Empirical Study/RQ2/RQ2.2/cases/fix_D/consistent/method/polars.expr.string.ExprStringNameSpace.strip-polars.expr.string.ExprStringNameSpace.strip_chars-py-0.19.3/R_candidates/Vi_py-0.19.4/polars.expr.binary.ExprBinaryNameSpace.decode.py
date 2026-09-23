    def decode(self, encoding: TransferEncoding, *, strict: bool = True) -> Expr:
        """
        Decode a value using the provided encoding.

        Parameters
        ----------
        encoding : {'hex', 'base64'}
            The encoding to use.
        strict
            Raise an error if the underlying value cannot be decoded,
            otherwise mask out with a null value.

        """
        if encoding == "hex":
            return wrap_expr(self._pyexpr.bin_hex_decode(strict))
        elif encoding == "base64":
            return wrap_expr(self._pyexpr.bin_base64_decode(strict))
        else:
            raise ValueError(
                f"encoding must be one of {{'hex', 'base64'}}, got {encoding!r}"
            )
