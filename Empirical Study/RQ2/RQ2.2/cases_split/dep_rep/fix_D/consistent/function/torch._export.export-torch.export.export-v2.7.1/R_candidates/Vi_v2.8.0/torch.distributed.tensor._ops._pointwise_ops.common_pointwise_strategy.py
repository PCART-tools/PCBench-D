def common_pointwise_strategy(
    args_schema: Sequence[object],
    followed_strategy: OpStrategy,
    linearity: bool,
) -> OpStrategy:
    # handle broadcasting
    common_shape = torch.broadcast_shapes(
        *[arg.shape for arg in args_schema if isinstance(arg, OpStrategy)]
    )
    pointwise_strategy = OpStrategy([])

    for placement_strategy in followed_strategy.strategies:
        spec_to_follow = placement_strategy.output_spec
        out_placements: list[Placement] = []
        for placement in spec_to_follow.placements:
            if isinstance(placement, Shard):
                shard_dim = normalize_dim(placement.dim, len(spec_to_follow.shape))
                common_ndim = len(common_shape)
                new_shard_dim = common_ndim - len(spec_to_follow.shape) + shard_dim
                out_placements.append(Shard(new_shard_dim))
            elif isinstance(placement, Partial) and not linearity:
                # clear the partial placemnet if op does not support linearity
                # by default we just replicate the partial, need to see if this
                # is optimal for all cases
                out_placements.append(Replicate())
            else:
                out_placements.append(placement)

        input_specs: list[DTensorSpec] = []
        redistribute_costs: list[list[float]] = []
        for arg_idx, input_arg in enumerate(args_schema):
            if isinstance(input_arg, OpStrategy):
                # sanity check that all args that follow the same strategy
                # are on the same DeviceMesh
                if input_arg.mesh != followed_strategy.mesh:
                    raise ValueError(
                        f"Could not run pointwise computation across different mesh: "
                        f"Found {input_arg.mesh} and {followed_strategy.mesh}!"
                    )

                # every arg follow the out_placements, but need to handle broadcasting
                input_arg_spec = input_arg.strategies[0].output_spec
                input_arg_dims_map = infer_broadcast_dims_map(
                    common_shape, input_arg_spec.shape
                )
                input_target_placements = map_placements_after_broadcast(
                    tuple(out_placements),
                    common_shape,
                    input_arg_dims_map,
                )
                input_arg_target_spec = DTensorSpec(
                    mesh=followed_strategy.mesh,
                    placements=input_target_placements,
                    tensor_meta=input_arg_spec.tensor_meta,
                )
                input_specs.append(input_arg_target_spec)
                redistribute_costs.append(
                    generate_redistribute_costs(input_arg, input_arg_target_spec)
                )

        pointwise_strategy.strategies.append(
            OpSpec(
                output_specs=DTensorSpec(
                    mesh=followed_strategy.mesh,
                    placements=tuple(out_placements),
                ),
                input_specs=input_specs,
                redistribute_cost=redistribute_costs,
            )
        )
    return pointwise_strategy
