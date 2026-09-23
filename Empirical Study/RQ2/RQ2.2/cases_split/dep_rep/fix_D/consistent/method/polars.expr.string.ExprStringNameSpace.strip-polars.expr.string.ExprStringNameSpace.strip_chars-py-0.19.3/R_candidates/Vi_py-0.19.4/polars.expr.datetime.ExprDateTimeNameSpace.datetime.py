    def datetime(self) -> Expr:
        """
        Return datetime.

        Applies to Datetime columns.

        Returns
        -------
        Expr
            Expression of data type :class:`Datetime`.

        """
        return wrap_expr(self._pyexpr.dt_datetime())
