def pointwise_strategy(op_schema: OpSchema, linearity: bool = False) -> OpStrategy:
    max_shards_strategy_index = -1
    max_shards = -1

    if _is_inplace_op(op_schema.op):
        # inplace op should follow the first arg strategy
        followed_strategy = op_schema.args_schema[0]
    elif _is_out_variant_op(op_schema.op):
        # out variant op should follow the out kwarg strategy
        followed_strategy = op_schema.kwargs_schema["out"]
    else:
        # normal pointwise op, we choose to follow the arg with
        # the max shards in case operands needs reshard
        for idx, arg_strategy in enumerate(op_schema.args_schema):
            if not isinstance(arg_strategy, OpStrategy):
                continue

            arg_max_shards = arg_strategy.max_num_shards()
            if arg_max_shards > max_shards:
                max_shards_strategy_index = idx
                max_shards = arg_max_shards

        followed_strategy = op_schema.args_schema[max_shards_strategy_index]

    assert isinstance(followed_strategy, OpStrategy), (
        f"no strategy to follow for {op_schema}!"
    )
    return common_pointwise_strategy(
        op_schema.args_schema, followed_strategy, linearity
    )
