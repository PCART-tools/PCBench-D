@register_op_strategy(aten.t.default)
def transpose_strategy(op_schema: OpSchema) -> OpStrategy:
    self_strategy = op_schema.args_schema[0]
    assert isinstance(self_strategy, OpStrategy)

    transpose_strategies = []
    for input_strategy in self_strategy.strategies:
        input_spec = input_strategy.output_spec
        # follow the input spec but transpose the Shard placements
        output_placements = [
            Shard(1 - p.dim) if isinstance(p, Shard) else p
            for p in input_spec.placements
        ]
        transpose_strategy = PlacementStrategy(
            output_specs=DTensorSpec(
                mesh=input_strategy.mesh,
                placements=tuple(output_placements),
            ),
            input_specs=(input_strategy.output_spec,),
        )
        transpose_strategies.append(transpose_strategy)

    return OpStrategy(strategies=transpose_strategies)
