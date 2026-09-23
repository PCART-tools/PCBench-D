    def nanosecond(self) -> Expr:
        """
        Extract nanoseconds from underlying DateTime representation.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Int32`.

        """
        return wrap_expr(self._pyexpr.dt_nanosecond())
