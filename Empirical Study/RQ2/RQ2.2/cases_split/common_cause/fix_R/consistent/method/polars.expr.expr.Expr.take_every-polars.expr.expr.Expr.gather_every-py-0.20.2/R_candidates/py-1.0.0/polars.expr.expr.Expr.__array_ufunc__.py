    def __array_ufunc__(
        self, ufunc: Callable[..., Any], method: str, *inputs: Any, **kwargs: Any
    ) -> Expr:
        """Numpy universal functions."""
        if method != "__call__":
            msg = f"Only call is implemented not {method}"
            raise NotImplementedError(msg)
        # Numpy/Scipy ufuncs have signature None but numba signatures always exists.
        is_custom_ufunc = getattr(ufunc, "signature") is not None  # noqa: B009
        num_expr = sum(isinstance(inp, Expr) for inp in inputs)
        exprs = [
            (inp, Expr, i) if isinstance(inp, Expr) else (inp, None, i)
            for i, inp in enumerate(inputs)
        ]
        if num_expr == 1:
            root_expr = next(expr[0] for expr in exprs if expr[1] == Expr)
        else:
            root_expr = F.struct(expr[0] for expr in exprs if expr[1] == Expr)

        def function(s: Series) -> Series:  # pragma: no cover
            args = []
            for i, expr in enumerate(exprs):
                if expr[1] == Expr and num_expr > 1:
                    args.append(s.struct[i])
                elif expr[1] == Expr:
                    args.append(s)
                else:
                    args.append(expr[0])
            return ufunc(*args, **kwargs)

        if is_custom_ufunc is True:
            msg = (
                "Native numpy ufuncs are dispatched using `map_batches(ufunc, is_elementwise=True)` which "
                "is safe for native Numpy and Scipy ufuncs but custom ufuncs in a group_by "
                "context won't be properly grouped. Custom ufuncs are dispatched with is_elementwise=False. "
                f"If {ufunc.__name__} needs elementwise then please use map_batches directly."
            )
            warnings.warn(
                msg,
                CustomUFuncWarning,
                stacklevel=find_stacklevel(),
            )
            return root_expr.map_batches(
                function, is_elementwise=False
            ).meta.undo_aliases()
        return root_expr.map_batches(function, is_elementwise=True).meta.undo_aliases()
