def register_op_strategy_map(
    aten_op_overload: torch._ops.OpOverload,
    local_op_name: Callable[..., torch.Tensor],
    schema_info: Optional[RuntimeSchemaInfo] = None,
) -> None:
    dim_map: Callable[..., DimMap] = dim_maps[local_op_name]

    @register_op_strategy(aten_op_overload, schema_info=schema_info)
    def reshape_strategy(op_schema: OpSchema) -> StrategyType:
        rules = dim_map(*op_schema.args_schema, **op_schema.kwargs_schema)
        input_strategy = cast(OpStrategy, op_schema.args_schema[0])
        mesh = op_schema.get_mesh_from_args(validate=False)

        global_in_shape = input_strategy.shape
        assert global_in_shape is not None, "Shape required."

        output_strategy = OpStrategy([])
        for input_placement_strategy in input_strategy.strategies:
            input_src_spec = input_placement_strategy.output_spec

            input_tgt_placements, output_placements = propagate_shape_and_sharding(
                input_src_spec.placements,
                tuple(global_in_shape),
                rules,
                mesh.shape,
            )

            # TODO: optimize this. we shouldn't simply blindly replicate
            #       unshardable dims ...
            # FIXME: this can be wrong for situations where we have
            #        [Shard(0), Shard(0)]
            input_tgt_spec = DTensorSpec(
                placements=tuple(input_tgt_placements),
                mesh=mesh,
                tensor_meta=input_src_spec.tensor_meta,
            )
            redistribute_costs = [
                generate_redistribute_costs(input_strategy, input_tgt_spec)
            ]

            output_spec = DTensorSpec(mesh=mesh, placements=tuple(output_placements))
            output_strategy.strategies.append(
                PlacementStrategy(
                    output_specs=output_spec,
                    input_specs=(input_tgt_spec,),
                    redistribute_cost=redistribute_costs,
                )
            )

        return output_strategy
