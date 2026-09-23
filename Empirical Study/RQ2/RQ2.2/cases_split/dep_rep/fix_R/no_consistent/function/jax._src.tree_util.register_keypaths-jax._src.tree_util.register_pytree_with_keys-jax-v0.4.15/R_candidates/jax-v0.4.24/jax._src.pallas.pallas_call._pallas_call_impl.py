def _pallas_call_impl(*args, jaxpr, name, out_shapes, which_linear,
                      interpret, debug: bool,
                      in_shapes,
                      input_output_aliases: tuple[tuple[int, int], ...],
                      grid_mapping: GridMapping,
                      **compiler_params: Any):
  dynamic_grid_args, args = split_list(  # type: ignore
      args, [grid_mapping.num_dynamic_grid_bounds]
  )
  if interpret:
    # If we're in interpreter mode, we *scan* over the grid and eval the
    # discharged jaxpr. This should reproduce exactly what compiling to Triton
    # will do.
    dynamic_grid_args_iter = iter(dynamic_grid_args)
    grid = tuple(
        a if a is not None else next(dynamic_grid_args_iter)
        for a in grid_mapping.grid
    )
    assert next(dynamic_grid_args_iter, None) is None
    discharged_jaxpr, consts = state_discharge.discharge_state(jaxpr, ())
    if debug:
      print(discharged_jaxpr)
    oi_map = {v: k for k, v in input_output_aliases}
    out = []
    for i, out_shape in enumerate(out_shapes):
      if i in oi_map:
        out.append(args[oi_map[i]])
      else:
        # TODO(sharadmv): use unitialized values for outputs
        out.append(jnp.zeros(out_shape.shape, out_shape.dtype))
    scalars, args = split_list(args, [grid_mapping.num_index_operands])  # type: ignore
    # invars: [*scalar_prefetch, *inputs, *outputs, *scratch]
    num_invars = len(jaxpr.invars)
    num_inputs_outputs = (
        num_invars
        - grid_mapping.num_index_operands
        - grid_mapping.num_scratch_operands
    )
    _, _, scratch_invars = split_list(
        jaxpr.invars, [grid_mapping.num_index_operands, num_inputs_outputs]
    )
    scratch_avals = [v.aval for v in scratch_invars]
    if not all(
        hasattr(a, "shape") and hasattr(a, "dtype") for a in scratch_avals
    ):
      raise NotImplementedError(f"Cannot initialize scratch: {scratch_avals}")
    scratch_values = [_uninitialized_value(a.shape, a.dtype)
                      for a in scratch_avals]
    carry = [*args, *out, *scratch_values]
    num_carry = len(args) + len(out)
    grid_start_indices = (jnp.int32(0),) * len(grid)
    if grid:
      num_iterations = reduce(jnp.multiply, grid)
    else:
      # Base case is always one iteration when grid is ()
      num_iterations = 1
    def cond(carry):
      i, *_ = carry
      return i < num_iterations
    def body(carry):
      i, loop_idx, *carry = carry
      carry, scratch = split_list(carry, [num_carry])
      start_indices = [
          None if bm is None else bm.compute_start_indices(loop_idx, *scalars)
          for bm in grid_mapping.block_mappings]
      block_shapes_without_mapped_dims = [
          None if block_mapping is None else block_mapping.block_shape
          for block_mapping in grid_mapping.block_mappings
      ]
      is_indexing_dim = [
          None if bm is None else tuple(b is pallas_core.mapped for b in bm)
          for bm in block_shapes_without_mapped_dims
      ]
      block_shapes = [
          None if bm is None else tuple(1 if i else b for i, b in zip(iid, bm))
          for iid, bm in zip(is_indexing_dim, block_shapes_without_mapped_dims)
      ]
      blocks = map(_maybe_dynamic_slice, start_indices, block_shapes, carry,
                   is_indexing_dim)
      is_mapped_grid_dim = [
          i in grid_mapping.mapped_dims for i in range(len(grid_mapping.grid))]
      local_grid_env, _ = partition_list(is_mapped_grid_dim,
                                         zip(loop_idx, grid_mapping.grid))
      with pallas_core.grid_env(tuple(local_grid_env)):
        assert len(discharged_jaxpr.invars) == len(scalars) + len(blocks) + len(
            scratch_values
        ), (
            len(discharged_jaxpr.invars),
            len(scalars),
            len(blocks),
            len(scratch_values),
        )
        blocks = jax.core.eval_jaxpr(discharged_jaxpr, consts, *scalars,
                                     *blocks, *scratch)
      blocks = blocks[grid_mapping.num_index_operands:]
      blocks, out_scratch = split_list(blocks, [num_carry])
      carry = map(_maybe_dynamic_update_slice, start_indices, block_shapes,
                  carry, blocks, is_indexing_dim)
      return (i + 1, _get_next_indices(grid, loop_idx), *carry, *out_scratch)
    (_, _, *carry) = lax.while_loop(
        cond, body, (jnp.int32(0), grid_start_indices, *carry)
    )
    _, out, _ = split_list(carry, [len(args), len(out)])
    return out
  return xla.apply_primitive(pallas_call_p, *args, jaxpr=jaxpr, name=name,
                             in_shapes=in_shapes,
                             out_shapes=out_shapes, which_linear=which_linear,
                             grid_mapping=grid_mapping, interpret=interpret,
                             debug=debug,
                             input_output_aliases=input_output_aliases,
                             **compiler_params)
