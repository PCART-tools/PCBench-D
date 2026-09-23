def list_pointwise_strategy(
    op_schema: OpSchema, linearity: bool = False
) -> StrategyType:
    """
    Apply the pointwise strategy to the zipped arguments. For example, if we
    run a foreach add of two lists l1 and l2, then we apply the pointwise
    strategy on each pair (l1[i], l2[i]). If the first argument is a list but
    the second (or later) one is a tensor, then we broadcast the tensor by
    replicating it into a list with the length of the first argument.

    Args:
        mesh (DeviceMesh): device mesh for pointwise ops
        op_schema (OpSchema): schema of the operator to generate strategy for
        linearity (bool): specify whether op(a) + op(b) = op(a + b)

    Returns:
        OpStrategy: generated strategy
    """

    def args_tuple_strategies(args_schema: tuple[object, ...]) -> list[TupleStrategy]:
        first_arg = args_schema[0]
        assert isinstance(first_arg, TupleStrategy)
        strategy_len = len(first_arg.childs)
        tuple_strategies: list[TupleStrategy] = []
        for arg_idx, arg in enumerate(args_schema):
            if isinstance(arg, TupleStrategy):
                # every tuple strategy should have the same length
                assert len(arg.childs) == strategy_len
                tuple_strategies.append(arg)
            elif isinstance(arg, OpStrategy):
                if arg_idx > 0:  # implicitly broadcast
                    tuple_strategies.append(
                        TupleStrategy([arg for _ in range(strategy_len)])
                    )
                else:
                    raise RuntimeError(
                        f"list op only supports tuple strategy! {op_schema}"
                    )
        return tuple_strategies

    args_strategies = args_tuple_strategies(op_schema.args_schema)
    follow_strategy: TupleStrategy = args_strategies[0]
    list_strategy: list[OpStrategy] = []
    for child_idx, child_strtgy in enumerate(follow_strategy.childs):
        assert isinstance(child_strtgy, OpStrategy)
        args_schema: list[OpStrategy] = [
            cast(OpStrategy, arg_strategy.childs[child_idx])
            for arg_strategy in args_strategies
        ]
        pointwise_strategy: OpStrategy = common_pointwise_strategy(
            args_schema, child_strtgy, linearity
        )
        list_strategy.append(pointwise_strategy)
    return TupleStrategy(list_strategy)
