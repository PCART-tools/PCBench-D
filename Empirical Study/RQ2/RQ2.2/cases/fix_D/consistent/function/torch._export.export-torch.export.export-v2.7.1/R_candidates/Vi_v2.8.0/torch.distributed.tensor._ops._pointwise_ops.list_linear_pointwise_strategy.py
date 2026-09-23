def list_linear_pointwise_strategy(op_schema: OpSchema) -> StrategyType:
    """
    for each list op stratgy that supports linearity
    """
    return list_pointwise_strategy(op_schema, linearity=True)
