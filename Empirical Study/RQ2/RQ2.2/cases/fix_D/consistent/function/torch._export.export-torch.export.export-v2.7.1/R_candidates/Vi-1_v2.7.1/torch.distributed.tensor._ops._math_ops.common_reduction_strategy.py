def common_reduction_strategy(
    input_strategy: OpStrategy,
    reduce_dims: list[int],
    keep_dim: bool = False,
    reduction_linear: bool = True,
    reduction_op: ReductionOpType = "sum",
) -> OpStrategy:
    """
    reduction_linear means that the reduction `f` follows this rule:
        f([f(a), f(b)]) = f([a, b])

    reduction linear should be super set of linearity.
    """
    # by default follow reduction input strategy
    reduction_strategy = OpStrategy([])

    for strtg in input_strategy.strategies:
        if not reduction_linear:
            # input placements for this strategy should clear out pending sum and sharding
            # on the reduction dimension
            input_placements = replicate_reduction_dims(
                strtg.output_spec.placements, reduce_dims
            )
        else:
            input_placements = strtg.output_spec.placements

        input_spec = DTensorSpec(
            mesh=input_strategy.mesh,
            placements=input_placements,
            tensor_meta=strtg.output_spec.tensor_meta,
        )

        reduce_dims_map = _infer_reduce_dims_map(reduce_dims, input_spec.ndim, keep_dim)
        out_placements = map_placements_after_reduction(
            input_spec.placements, reduce_dims, reduce_dims_map, reduction_op
        )
        redistribute_cost = [generate_redistribute_costs(input_strategy, input_spec)]
        reduction_strategy.strategies.append(
            PlacementStrategy(
                output_specs=DTensorSpec(
                    mesh=input_strategy.mesh,
                    placements=out_placements,
                ),
                input_specs=(input_spec,),
                redistribute_cost=redistribute_cost,
            )
        )

    return reduction_strategy
