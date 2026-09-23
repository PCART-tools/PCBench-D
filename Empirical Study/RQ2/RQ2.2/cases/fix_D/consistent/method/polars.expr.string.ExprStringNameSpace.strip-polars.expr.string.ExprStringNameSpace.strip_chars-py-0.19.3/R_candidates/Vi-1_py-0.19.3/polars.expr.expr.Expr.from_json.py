    @classmethod
    def from_json(cls, value: str) -> Self:
        """
        Read an expression from a JSON encoded string to construct an Expression.

        Parameters
        ----------
        value
            JSON encoded string value

        """
        expr = cls.__new__(cls)
        expr._pyexpr = PyExpr.meta_read_json(value)
        return expr
