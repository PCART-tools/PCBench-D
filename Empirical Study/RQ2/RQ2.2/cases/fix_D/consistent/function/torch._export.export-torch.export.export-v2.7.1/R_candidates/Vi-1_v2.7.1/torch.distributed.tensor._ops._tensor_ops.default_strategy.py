def default_strategy(op_schema: OpSchema) -> StrategyType:
    # Default strategy by default just propagate the first input strategy
    select_strategy = op_schema.args_schema[0]
    assert isinstance(select_strategy, OpStrategy)
    # we create new DTensorSpecs even for default strategy to assure that
    # the tensor metas are distinct between the arguments and outputs
    default_strategy = [
        PlacementStrategy(
            output_specs=DTensorSpec(
                mesh=select_strategy.mesh,
                placements=strategy.output_spec.placements,
            )
        )
        for strategy in select_strategy.strategies
    ]
    return OpStrategy(default_strategy)
