def pointwise_strategy(op_schema: OpSchema, linearity: bool = False) -> OpStrategy:
    max_shards_strategy_index = -1
    max_shards = -1
    max_ndim = -1

    if op_schema.is_inplace_op():
        # inplace op should follow the first arg strategy
        followed_strategy = op_schema.args_schema[0]
    elif op_schema.is_out_variant_op():
        # out variant op should follow the out kwarg strategy
        followed_strategy = op_schema.kwargs_schema["out"]
    else:
        # normal pointwise op, we choose to follow the arg with
        # the max shards in case operands needs reshard
        # in case of multiple operands with max shard, we take
        # the one with the max number of dimensions
        for idx, arg_strategy in enumerate(op_schema.args_schema):
            if not isinstance(arg_strategy, OpStrategy):
                continue

            arg_max_shards = arg_strategy.max_num_shards()
            arg_max_ndim = arg_strategy.ndim
            if (arg_max_shards > max_shards) or (
                arg_max_shards == max_shards and arg_max_ndim > max_ndim
            ):
                max_shards_strategy_index = idx
                max_shards = arg_max_shards
                max_ndim = arg_max_ndim

        followed_strategy = op_schema.args_schema[max_shards_strategy_index]

    assert isinstance(followed_strategy, OpStrategy), (
        f"no strategy to follow for {op_schema}!"
    )
    return common_pointwise_strategy(
        op_schema.args_schema, followed_strategy, linearity
    )
