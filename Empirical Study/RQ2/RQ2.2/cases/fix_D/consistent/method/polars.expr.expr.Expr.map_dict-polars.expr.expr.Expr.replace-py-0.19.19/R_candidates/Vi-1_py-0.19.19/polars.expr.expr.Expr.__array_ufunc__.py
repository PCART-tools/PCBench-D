    def __array_ufunc__(
        self, ufunc: Callable[..., Any], method: str, *inputs: Any, **kwargs: Any
    ) -> Self:
        """Numpy universal functions."""
        num_expr = sum(isinstance(inp, Expr) for inp in inputs)
        if num_expr > 1:
            if num_expr < len(inputs):
                raise ValueError(
                    "NumPy ufunc with more than one expression can only be used"
                    " if all non-expression inputs are provided as keyword arguments only"
                )

            exprs = parse_as_list_of_expressions(inputs)
            return self._from_pyexpr(pyreduce(partial(ufunc, **kwargs), exprs))

        def function(s: Series) -> Series:  # pragma: no cover
            args = [inp if not isinstance(inp, Expr) else s for inp in inputs]
            return ufunc(*args, **kwargs)

        return self.map_batches(function)
