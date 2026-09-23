    def time(self) -> Expr:
        """
        Extract time.

        Applies to Datetime columns only; fails on Date.

        Returns
        -------
        Expr
            Expression of data type :class:`Time`.

        """
        return wrap_expr(self._pyexpr.dt_time())
