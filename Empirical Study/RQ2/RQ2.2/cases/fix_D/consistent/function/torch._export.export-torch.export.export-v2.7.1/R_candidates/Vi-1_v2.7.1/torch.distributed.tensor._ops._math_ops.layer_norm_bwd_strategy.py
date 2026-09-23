@register_op_strategy(
    [aten.native_layer_norm_backward.default],
    schema_info=RuntimeSchemaInfo(2),
)
def layer_norm_bwd_strategy(op_schema: OpSchema) -> OpStrategy:
    # backward op does not need to validate the mesh since forward op has already done it
    mesh = op_schema.get_mesh_from_args(validate=False)

    # args must be: grad_out, input, normalized_shape, mean, rstd,
    # weight, bias, output_mask. For None weight and bias, their
    # corresponding objects will be None as well.

    assert len(op_schema.args_schema) == 8
    (
        grad_out_strategy,
        input_strategy,
        normalized_shape,
        mean_strategy,
        rstd_strategy,
        weight_strategy,
        bias_strategy,
        output_mask,
    ) = op_schema.args_schema

    assert isinstance(grad_out_strategy, OpStrategy)
    assert isinstance(input_strategy, OpStrategy)
    assert isinstance(mean_strategy, OpStrategy)
    assert isinstance(rstd_strategy, OpStrategy)

    assert isinstance(normalized_shape, (int, Sequence, torch.Size))
    normalized_size = normalize_to_torch_size(normalized_shape)
    input_ndim = input_strategy.ndim
    axis = input_ndim - len(normalized_size)
    outer_dims = list(range(axis))

    assert isinstance(output_mask, list) and len(output_mask) == 3

    # output triple: (d_input, d_weight, d_bias)
    out_tuple_strategy = OpStrategy([])
    for idx, input_placement_strategy in enumerate(input_strategy.strategies):
        # args for PlacementStrategy
        output_specs_list: list[Optional[DTensorSpec]] = []
        input_specs_list: list[DTensorSpec] = []
        redistribute_costs = []

        input_src_spec = input_placement_strategy.output_spec
        # arg: grad_out
        # TODO: change the strategy to the following rule.
        # d_input is basically a product of element-wise mul of
        # grad_out, rstd, and normalized input, among which rstd
        # and normalized input (x_hat) should have the same sharding
        # placements, and grad_out's sharding is determined by the
        # pointwise result of x_hat and weight/bias.
        # TODO: now grad_out spec follows input spec. we may need
        # to change it to apply a pointwise rule over grad_out,
        # input, and weight.
        grad_out_target_spec = DTensorSpec(
            mesh=mesh,
            placements=_replicate_dims_start_at(input_src_spec.placements, axis),
            tensor_meta=input_src_spec.tensor_meta,
        )
        input_specs_list.append(grad_out_target_spec)
        redistribute_costs.append(
            generate_redistribute_costs(grad_out_strategy, grad_out_target_spec)
        )
        output_specs_list.append(grad_out_target_spec if output_mask[0] else None)

        # arg: input
        input_target_spec = DTensorSpec(
            mesh=mesh,
            placements=_replicate_dims_start_at(input_src_spec.placements, axis),
            tensor_meta=input_src_spec.tensor_meta,
        )
        input_specs_list.append(input_target_spec)
        redistribute_costs.append(
            generate_redistribute_costs(input_strategy, input_target_spec)
        )

        # arg: mean, rstd
        mean_src_spec = mean_strategy.strategies[idx].output_spec
        input_specs_list.append(mean_src_spec)
        redistribute_costs.append([0.0 for _ in mean_strategy.strategies])
        rstd_src_spec = rstd_strategy.strategies[idx].output_spec
        input_specs_list.append(rstd_src_spec)
        redistribute_costs.append([0.0 for _ in rstd_strategy.strategies])

        def _add_target_input_spec(strategy) -> DTensorSpec:
            # shared logic for setting the weight and bias target input specs
            assert isinstance(strategy, OpStrategy)
            src_spec = strategy.strategies[idx].output_spec
            # no need to redistribute since they should be replicated in forward pass
            input_specs_list.append(src_spec)
            redistribute_costs.append([0.0 for _ in strategy.strategies])
            return src_spec

        # arg: weight
        # d_weight = sum(grad_out * (input - mean) / rstd, outer_dim, keepdim=False)
        if weight_strategy is not None:
            weight_src_spec = _add_target_input_spec(weight_strategy)
            # TODO: now d_weight spec follows input spec w/ a reduction.
            # we may need to change to a pointwise rule over grad_out and
            # input, then apply a reduction.
            inp_placements = _replicate_dims_start_at(input_src_spec.placements, axis)
            reduce_dims_map = _infer_reduce_dims_map(
                outer_dims, input_src_spec.ndim, False
            )
            out_placements = map_placements_after_reduction(
                inp_placements, outer_dims, reduce_dims_map, "sum"
            )
            weight_out_spec = DTensorSpec(
                mesh=mesh,
                placements=out_placements,
                tensor_meta=weight_src_spec.tensor_meta,
            )
            output_specs_list.append(weight_out_spec if output_mask[1] else None)
        else:
            assert output_mask[1] is False, (
                "output_mask[1] should not be `True` while weight argument is `None` in native_layer_norm_backward."
            )
            output_specs_list.append(None)

        # arg: bias
        # d_bias = sum(grad_out, outer_dim, keepdim=False)
        if bias_strategy is not None:
            bias_src_spec = _add_target_input_spec(bias_strategy)
            # d_bias spec follows a reduction over grad_out
            inp_placements = _replicate_dims_start_at(
                grad_out_target_spec.placements, axis
            )
            reduce_dims_map = _infer_reduce_dims_map(
                outer_dims, grad_out_target_spec.ndim, False
            )
            out_placements = map_placements_after_reduction(
                inp_placements, outer_dims, reduce_dims_map, "sum"
            )
            bias_out_spec = DTensorSpec(
                mesh=mesh,
                placements=out_placements,
                tensor_meta=bias_src_spec.tensor_meta,
            )
            output_specs_list.append(bias_out_spec if output_mask[2] else None)
        else:
            assert output_mask[2] is False, (
                "output_mask[2] should not be `True` while bias argument is `None` in native_layer_norm_backward."
            )
            output_specs_list.append(None)

        out_tuple_strategy.strategies.append(
            PlacementStrategy(
                output_specs=tuple(output_specs_list),
                input_specs=input_specs_list,
                redistribute_cost=redistribute_costs,
            )
        )

    return out_tuple_strategy
