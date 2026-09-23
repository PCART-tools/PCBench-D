    @deprecate_renamed_function("register_plugin", version="0.19.12")
    def _register_plugin(
        self,
        *,
        lib: str,
        symbol: str,
        args: list[IntoExpr] | None = None,
        kwargs: dict[Any, Any] | None = None,
        is_elementwise: bool = False,
        input_wildcard_expansion: bool = False,
        auto_explode: bool = False,
        cast_to_supertypes: bool = False,
    ) -> Self:
        return self.register_plugin(
            lib=lib,
            symbol=symbol,
            args=args,
            kwargs=kwargs,
            is_elementwise=is_elementwise,
            input_wildcard_expansion=input_wildcard_expansion,
            returns_scalar=auto_explode,
            cast_to_supertypes=cast_to_supertypes,
        )
