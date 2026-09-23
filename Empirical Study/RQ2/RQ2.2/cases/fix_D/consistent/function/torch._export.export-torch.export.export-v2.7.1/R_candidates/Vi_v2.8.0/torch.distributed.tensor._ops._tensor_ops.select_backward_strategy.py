@register_op_strategy(
    aten.select_backward.default,
    schema_info=RuntimeSchemaInfo(1),
)
def select_backward_strategy(op_schema: OpSchema) -> OpStrategy:
    # func: select_backward(Tensor grad_output, SymInt[] input_sizes, int dim, SymInt index) -> Tensor
    args_schema = op_schema.args_schema
    input_strategy, dim = args_schema[0], args_schema[2]
    assert isinstance(input_strategy, OpStrategy), f"{input_strategy}"
    assert isinstance(dim, int)
    output_strategies: list[OpSpec] = []
    for placement_strategy in input_strategy.strategies:
        input_spec = placement_strategy.output_spec
        output_spec_placements: list[Placement] = []
        for placement in input_spec.placements:
            if isinstance(placement, Shard):
                shard_dim = placement.dim
                if shard_dim >= dim:
                    # NOTE: shard_dim is guaranteed to exist because
                    # grad_input has one more dim than grad_output
                    output_spec_placements.append(Shard(shard_dim + 1))
                else:
                    output_spec_placements.append(Shard(shard_dim))
            else:
                output_spec_placements.append(placement)
        output_specs = DTensorSpec(input_spec.mesh, tuple(output_spec_placements))
        output_strategies.append(
            OpSpec(output_specs=output_specs, input_specs=(input_spec,))
        )
    return OpStrategy(output_strategies)
