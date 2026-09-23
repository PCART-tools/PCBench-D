def register_prop_rule(
    op: Union[torch._ops.OpOverload, list[torch._ops.OpOverload]],
    schema_info: Optional[RuntimeSchemaInfo] = None,
) -> Callable[
    [Callable[[OpSchema], OutputSharding]], Callable[[OpSchema], OutputSharding]
]:
    # pyre-fixme[53]: Captured variable `func` is not annotated.
    # pyre-fixme[3]: Return type must be annotated.
    # pyre-fixme[2]: Parameter must be annotated.
    def wrapper(
        impl: Callable[[OpSchema], OutputSharding],
    ) -> Callable[[OpSchema], OutputSharding]:
        overloads = op if isinstance(op, list) else [op]
        for overload in overloads:
            DTensor._op_dispatcher.sharding_propagator.register_sharding_prop_rule(
                overload, impl, schema_info
            )
        return impl

    return wrapper
