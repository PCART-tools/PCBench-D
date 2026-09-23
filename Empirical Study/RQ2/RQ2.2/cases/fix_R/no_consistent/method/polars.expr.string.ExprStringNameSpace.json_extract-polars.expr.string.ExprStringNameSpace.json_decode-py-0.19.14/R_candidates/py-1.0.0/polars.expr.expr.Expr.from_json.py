    @classmethod
    def from_json(cls, value: str) -> Expr:
        """
        Read an expression from a JSON encoded string to construct an Expression.

        .. deprecated:: 0.20.11
            This method has been renamed to :meth:`deserialize`.
            Note that the new method operates on file-like inputs rather than strings.
            Enclose your input in `io.StringIO` to keep the same behavior.

        Parameters
        ----------
        value
            JSON encoded string value
        """
        issue_deprecation_warning(
            "`Expr.from_json` is deprecated. It has been renamed to `Expr.deserialize`."
            " Note that the new method operates on file-like inputs rather than strings."
            " Enclose your input in `io.StringIO` to keep the same behavior.",
            version="0.20.11",
        )
        return cls.deserialize(StringIO(value), format="json")
