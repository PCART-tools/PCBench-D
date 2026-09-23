def _pallas_call_impl(*args, jaxpr, name, out_shapes, which_linear,
                      interpret, debug: bool,
                      in_shapes,
                      input_output_aliases: Tuple[Tuple[int, int], ...],
                      grid_mapping: GridMapping,
                      **compiler_params: Any):
  if interpret:
    # If we're in interpreter mode, we *scan* over the grid and eval the
    # discharged jaxpr. This should reproduce exactly what compiling to Triton
    # will do.
    grid = grid_mapping.grid
    discharged_jaxpr, consts = state_discharge.discharge_state(jaxpr, ())
    if debug:
      print(discharged_jaxpr)
    loop_indices = jnp.array(list(it.product(*(range(g) for g in grid))))
    oi_map = {v: k for k, v in input_output_aliases}
    out = []
    for i, out_shape in enumerate(out_shapes):
      if i in oi_map:
        out.append(args[oi_map[i]])
      else:
        out.append(jnp.zeros(out_shape.shape, out_shape.dtype))
    scalars, args = split_list(args, [grid_mapping.num_index_operands])  # type: ignore
    carry = [*args, *out]
    def cond(carry):
      return carry[0] < loop_indices.shape[0]
    def body(carry):
      i, *carry = carry
      loop_idx = loop_indices[i]
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
        blocks = jax.core.eval_jaxpr(discharged_jaxpr, consts, *scalars,
                                     *blocks)
      blocks = blocks[grid_mapping.num_index_operands:]
      carry = map(_maybe_dynamic_update_slice, start_indices, block_shapes,
                  carry, blocks, is_indexing_dim)
      return (i + 1, *carry)
    (_, *carry) = lax.while_loop(cond, body, (0, *carry))
    _, out = split_list(carry, [len(args)])
    return out
  return xla.apply_primitive(pallas_call_p, *args, jaxpr=jaxpr, name=name,
                             in_shapes=in_shapes,
                             out_shapes=out_shapes, which_linear=which_linear,
                             grid_mapping=grid_mapping, interpret=interpret,
                             debug=debug,
                             input_output_aliases=input_output_aliases,
                             **compiler_params)
