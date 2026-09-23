@register_op_strategy(aten._local_scalar_dense.default)
def replica_only_strategy(op_schema: OpSchema) -> StrategyType:
    """Only allow replication on the input/output."""
    input_strategy = op_schema.args_schema[0]
    assert isinstance(input_strategy, OpStrategy)
    mesh = input_strategy.mesh
    replicate_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
    return OpStrategy([PlacementStrategy(replicate_spec)])
