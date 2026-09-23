    def date(self) -> Expr:
        """
        Extract date from date(time).

        Applies to Date and Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Date`.

        """
        return wrap_expr(self._pyexpr.dt_date())
