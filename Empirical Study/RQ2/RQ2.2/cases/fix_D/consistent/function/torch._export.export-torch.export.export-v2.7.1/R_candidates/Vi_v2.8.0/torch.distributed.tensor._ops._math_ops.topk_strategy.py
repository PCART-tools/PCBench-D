@register_op_strategy(
    [aten.topk.default],
    schema_info=RuntimeSchemaInfo(2),
)
def topk_strategy(op_schema: OpSchema) -> OpStrategy:
    input_strategy = cast(OpStrategy, op_schema.args_schema[0])
    topk_dim = (
        cast(int, op_schema.args_schema[2]) if len(op_schema.args_schema) > 2 else -1
    )
    topk_dim = normalize_dim(topk_dim, input_strategy.ndim)

    single_mesh_dim_strategies = []

    # two outputs (values, indices), 1 input
    # replicate always works
    all_replicate: PlacementList = [Replicate()] * 3
    single_mesh_dim_strategies.append(all_replicate)

    # every dim except topk dim should work
    for dim in range(input_strategy.ndim):
        if dim != topk_dim:
            dim_shardings: PlacementList = [Shard(dim)] * 3
            single_mesh_dim_strategies.append(dim_shardings)
    # TODO: topk on sharded dim requries non-trival reduction, address it later

    return expand_to_full_mesh_op_strategy(
        input_strategy.mesh, op_schema, single_mesh_dim_strategies, input_index=2
    )
