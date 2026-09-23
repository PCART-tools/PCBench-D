def expand_to_full_mesh_op_strategy(
    mesh: DeviceMesh,
    op_schema: OpSchema,
    single_mesh_dim_strategies: list[PlacementList],
    *,
    input_index: int = 1,
    inplace_op: bool = False,
) -> OpStrategy:
    # Expand the single_mesh_dim_strategies to full mesh dim strategies.
    all_mesh_dim_strategies = [single_mesh_dim_strategies] * mesh.ndim

    strategy_combs = itertools.product(*all_mesh_dim_strategies)

    all_strategies = []
    for strategy_comb in strategy_combs:
        spec_list: list[Optional[DTensorSpec]] = []
        for specs in zip(*strategy_comb):
            if specs[0] is not None:
                spec_list.append(DTensorSpec(mesh, specs))
            else:
                spec_list.append(None)

        input_specs: list[DTensorSpec] = [
            s for s in spec_list[input_index:] if isinstance(s, DTensorSpec)
        ]

        input_args_strategy = op_schema.args_strategy
        assert len(input_specs) == len(input_args_strategy)
        self_spec = input_args_strategy[0].strategies[0].output_spec

        if inplace_op and self_spec.placements != input_specs[0].placements:
            # if it's inplace op, we would only allow the OpSpec to be added when the
            # input_spec matches the first argument's runtime sharding, otherwise we skip
            continue

        # check inputs shardable
        inputs_shardable = all(
            is_tensor_shardable(inp.shape, s)
            for inp, s in zip(input_args_strategy, input_specs)
        )

        # only add to the all_strategies list when all inputs are shardable
        if inputs_shardable:
            redistribute_cost = [
                generate_redistribute_costs(input_strategy, input_spec)
                for input_strategy, input_spec in zip(input_args_strategy, input_specs)
            ]
            if input_index > 1:
                output_specs = tuple(spec_list[:input_index])
            else:
                if spec_list[0] is not None:
                    output_specs = spec_list[0]  # type: ignore[assignment]
                else:
                    raise RuntimeError("output spec is None")
            strategy = OpSpec(
                output_specs=output_specs,
                input_specs=input_specs,
                redistribute_cost=redistribute_cost,
            )
            all_strategies.append(strategy)

    return OpStrategy(all_strategies)
