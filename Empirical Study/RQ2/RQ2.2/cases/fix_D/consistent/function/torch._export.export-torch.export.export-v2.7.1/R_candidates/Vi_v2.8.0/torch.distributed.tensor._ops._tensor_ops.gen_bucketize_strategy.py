@register_op_strategy(aten.bucketize.Tensor)
def gen_bucketize_strategy(op_schema: OpSchema) -> StrategyType:
    """Just propagate input sharding, but expect replicated for boundaries input."""
    mesh = op_schema.get_mesh_from_args()
    input_strategy = op_schema.args_schema[0]
    bucketize_strategy = OpStrategy([])
    assert isinstance(input_strategy, OpStrategy)
    for arg_strategy in input_strategy.strategies:
        arg_spec = DTensorSpec(mesh, arg_strategy.output_spec.placements)
        replica_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
        bucketize_strategy.strategies.append(
            OpSpec(output_specs=arg_spec, input_specs=(arg_spec, replica_spec))
        )

    return bucketize_strategy
