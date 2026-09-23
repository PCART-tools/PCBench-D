    @deprecate_function(
        "Use `polars.plugins.register_plugin_function` instead.", version="0.20.16"
    )
    def register_plugin(
        self,
        *,
        lib: str,
        symbol: str,
        args: list[IntoExpr] | None = None,
        kwargs: dict[Any, Any] | None = None,
        is_elementwise: bool = False,
        input_wildcard_expansion: bool = False,
        returns_scalar: bool = False,
        cast_to_supertypes: bool = False,
        pass_name_to_apply: bool = False,
        changes_length: bool = False,
    ) -> Expr:
        """
        Register a plugin function.

        .. deprecated:: 0.20.16
            Use :func:`polars.plugins.register_plugin_function` instead.

        See the `user guide <https://docs.pola.rs/user-guide/expressions/plugins/>`_
        for more information about plugins.

        Warnings
        --------
        This method is deprecated. Use the new `polars.plugins.register_plugin_function`
        function instead.

        This is highly unsafe as this will call the C function loaded by
        `lib::symbol`.

        The parameters you set dictate how Polars will handle the function.
        Make sure they are correct!

        Parameters
        ----------
        lib
            Library to load.
        symbol
            Function to load.
        args
            Arguments (other than self) passed to this function.
            These arguments have to be of type Expression.
        kwargs
            Non-expression arguments. They must be JSON serializable.
        is_elementwise
            If the function only operates on scalars
            this will trigger fast paths.
        input_wildcard_expansion
            Expand expressions as input of this function.
        returns_scalar
            Automatically explode on unit length if it ran as final aggregation.
            this is the case for aggregations like `sum`, `min`, `covariance` etc.
        cast_to_supertypes
            Cast the input datatypes to their supertype.
        pass_name_to_apply
            if set, then the `Series` passed to the function in the group_by operation
            will ensure the name is set. This is an extra heap allocation per group.
        changes_length
            For example a `unique` or a `slice`
        """
        from polars.plugins import register_plugin_function

        if args is None:
            args = [self]
        else:
            args = [self, *list(args)]

        return register_plugin_function(
            plugin_path=lib,
            function_name=symbol,
            args=args,
            kwargs=kwargs,
            is_elementwise=is_elementwise,
            changes_length=changes_length,
            returns_scalar=returns_scalar,
            cast_to_supertype=cast_to_supertypes,
            input_wildcard_expansion=input_wildcard_expansion,
            pass_name_to_apply=pass_name_to_apply,
        )
