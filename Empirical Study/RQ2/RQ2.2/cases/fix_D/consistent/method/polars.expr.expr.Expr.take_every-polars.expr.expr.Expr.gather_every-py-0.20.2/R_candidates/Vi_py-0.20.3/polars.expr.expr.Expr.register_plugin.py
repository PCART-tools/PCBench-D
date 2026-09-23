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
    ) -> Self:
        """
        Register a shared library as a plugin.

        .. warning::
            This is highly unsafe as this will call the C function
            loaded by `lib::symbol`.

            The parameters you give dictate how polars will deal
            with the function. Make sure they are correct!

        .. note::
            This functionality is unstable and may change without it
            being considered breaking.

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
        if args is None:
            args = []
        else:
            args = [parse_as_expression(a) for a in args]
        if kwargs is None:
            serialized_kwargs = b""
        else:
            import pickle

            # Choose the highest protocol supported by https://docs.rs/serde-pickle/latest/serde_pickle/
            serialized_kwargs = pickle.dumps(kwargs, protocol=5)

        return self._from_pyexpr(
            self._pyexpr.register_plugin(
                lib,
                symbol,
                args,
                serialized_kwargs,
                is_elementwise,
                input_wildcard_expansion,
                returns_scalar,
                cast_to_supertypes,
                pass_name_to_apply,
                changes_length,
            )
        )
