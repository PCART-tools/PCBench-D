@register_op_strategy(aten.slice_backward.default)
def slice_backward_rules(op_schema: OpSchema) -> StrategyType:
    """
    slice_backward is a new_zeros + slice_scatter, we only allow replication
    on the input/output for now since new_zeros would produce replication
    """
    mesh = op_schema.get_mesh_from_args(validate=False)
    replicate_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
    return OpStrategy([PlacementStrategy(replicate_spec)])
