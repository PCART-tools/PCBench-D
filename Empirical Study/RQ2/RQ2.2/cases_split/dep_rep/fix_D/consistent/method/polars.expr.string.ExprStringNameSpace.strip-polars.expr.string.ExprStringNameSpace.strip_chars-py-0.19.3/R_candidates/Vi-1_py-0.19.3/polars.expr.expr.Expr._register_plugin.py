    def _register_plugin(
        self,
        lib: str,
        symbol: str,
        args: list[IntoExpr] | None = None,
        *,
        is_elementwise: bool = False,
        input_wildcard_expansion: bool = False,
        auto_explode: bool = False,
        cast_to_supertypes: bool = False,
    ) -> Self:
        """
        Register a shared library as a plugin.

        .. warning::
            This is highly unsafe as this will call the C function
            loaded by ``lib::symbol``

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
        is_elementwise
            If the function only operates on scalars
            this will trigger fast paths.
        input_wildcard_expansion
            Expand expressions as input of this function.
        auto_explode
            Explode the results in a group_by.
            This is recommended for aggregation functions.
        cast_to_supertypes
            Cast the input datatypes to their supertype.

        """
        if args is None:
            args = []
        else:
            args = [parse_as_expression(a) for a in args]
        return self._from_pyexpr(
            self._pyexpr.register_plugin(
                lib,
                symbol,
                args,
                is_elementwise,
                input_wildcard_expansion,
                auto_explode,
                cast_to_supertypes,
            )
        )
