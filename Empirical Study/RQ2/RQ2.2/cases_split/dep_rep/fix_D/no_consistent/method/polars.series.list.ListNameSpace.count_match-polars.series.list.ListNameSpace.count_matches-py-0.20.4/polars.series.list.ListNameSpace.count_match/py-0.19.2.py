    def count_match(
        self, element: float | str | bool | int | date | datetime | time | Expr
    ) -> Expr:
        """
        Count how often the value produced by ``element`` occurs.

        Parameters
        ----------
        element
            An expression that produces a single value

        """
