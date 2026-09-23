    def millisecond(self) -> Expr:
        """
        Extract milliseconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`UInt32`.

        """
        return wrap_expr(self._pyexpr.dt_millisecond())
