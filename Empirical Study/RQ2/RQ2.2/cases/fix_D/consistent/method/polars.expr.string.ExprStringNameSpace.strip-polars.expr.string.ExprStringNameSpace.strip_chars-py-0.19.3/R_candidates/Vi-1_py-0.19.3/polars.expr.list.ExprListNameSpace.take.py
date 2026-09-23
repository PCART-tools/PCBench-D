    def take(
        self,
        index: Expr | Series | list[int] | list[list[int]],
        *,
        null_on_oob: bool = False,
    ) -> Expr:
        """
        Take sublists by multiple indices.

        The indices may be defined in a single column, or by sublists in another
        column of dtype ``List``.

        Parameters
        ----------
        index
            Indices to return per sublist
        null_on_oob
            Behavior if an index is out of bounds:
            True -> set as null
            False -> raise an error
            Note that defaulting to raising an error is much cheaper

        """
        if isinstance(index, list):
            index = pl.Series(index)
        index = parse_as_expression(index)
        return wrap_expr(self._pyexpr.list_take(index, null_on_oob))
