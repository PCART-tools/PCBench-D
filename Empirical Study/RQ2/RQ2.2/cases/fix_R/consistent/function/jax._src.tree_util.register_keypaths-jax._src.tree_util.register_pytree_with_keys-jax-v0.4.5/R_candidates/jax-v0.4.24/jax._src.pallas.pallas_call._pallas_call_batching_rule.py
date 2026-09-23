def _pallas_call_batching_rule(args, dims, *,
                               jaxpr: jax_core.Jaxpr,
                               name: str,
                               in_shapes: tuple[jax.ShapeDtypeStruct, ...],
                               out_shapes: tuple[jax.ShapeDtypeStruct, ...],
                               grid_mapping: GridMapping,
                               input_output_aliases: tuple[tuple[int, int], ...],
                               debug: bool,
                               interpret: bool,
                               which_linear: tuple[bool, ...],
                               **compiler_params: Any):

  def _maybe_squeeze_out_bdim(
      x: jax.Array, bdim: int | batching.NotMapped
  ) -> jax.Array:
    if bdim is batching.not_mapped:
      return x
    return jnp.squeeze(x, axis=bdim)

  dynamic_grid_args, args = split_list(
      args, [grid_mapping.num_dynamic_grid_bounds]
  )
  dynamic_grid_dims, dims = split_list(
      dims, [grid_mapping.num_dynamic_grid_bounds]
  )
  if all(
      bdim is batching.not_mapped or arg.shape[bdim] == 1
      for arg, bdim in zip(dynamic_grid_args, dynamic_grid_dims)
  ):
    dynamic_grid_args = safe_map(
        _maybe_squeeze_out_bdim, dynamic_grid_args, dynamic_grid_dims)
  elif any(bdim is not batching.not_mapped for bdim in dynamic_grid_dims):
    raise NotImplementedError(
        f"Batched dynamic grid bounds unsupported: {dynamic_grid_dims}"
    )
  else:
    pass  # No dynamic grid dimensions
  del dynamic_grid_dims
  if grid_mapping.num_index_operands:
    scalar_args, args = split_list(args, [grid_mapping.num_index_operands])
    scalar_bdims, bdims = split_list(dims, [grid_mapping.num_index_operands])
    # Ordinarily, adding support for scalar prefetch in vmap would involve
    # modifying the block specs in a nontrivial way. However, if we are only
    # vmapping over 1-sized dimensions, we can just get rid of the dimensions
    # and pretend we were never vmapping over them at all.
    if all(
        bdim is batching.not_mapped or arg.shape[bdim] == 1
        for arg, bdim in zip(scalar_args, scalar_bdims)
    ):
      scalar_args = safe_map(_maybe_squeeze_out_bdim, scalar_args, scalar_bdims)
      scalar_bdims = [None] * len(scalar_args)
      args = (*scalar_args, *args)
      dims = (*scalar_bdims, *bdims)
    else:
      # TODO(sharadmv,apaszke): enable batching over prefetched scalar args
      raise NotImplementedError
  if not dims:
    raise NotImplementedError("vmapping pallas_call with no arguments.")
  axis_size, = {x.shape[d] for x, d in zip(args, dims)
                if d is not batching.not_mapped}
  block_mappings = grid_mapping.block_mappings
  avals = [v.aval for v in jaxpr.invars]
  # How should we pick output dimensions? This actually matters because XLA
  # can't optimize our pallas kernels, and this layout impacts performance. For
  # now, because `vmap` doesn't really offer a way of inferring good output
  # dimensions. For now, we just use 0.
  # TODO(sharadmv): explore inferring better output dimensions via a heuristic
  # TODO(sharadmv): explore a long term solution to output dim inference

  # When we have input/output aliasing, since the output will be mapped, we need
  # to make sure to broadcast the input across that dimension if it is not
  # mapped.
  dims_ = list(dims)
  args_ = list(args)
  for input_index, _ in input_output_aliases:
    dim = dims_[input_index]
    if dim is batching.not_mapped:
      dims_[input_index] = 0
      args_[input_index] = batching.broadcast(args_[input_index], axis_size, 0)
  args = tuple(args_)
  dims = tuple(dims_)

  all_dims = list(dims) + [0] * len(out_shapes)

  num_index_operands = grid_mapping.num_index_operands
  num_scratch_operands = grid_mapping.num_scratch_operands

  # Only add a batch dimension for the avals that actually have a grid mapping.
  # This excludes scalar prefetch inputs (the first in the list) and scratch
  # operands (the last in the list).
  avals_to_batch = avals[num_index_operands:(len(avals) - num_scratch_operands)]
  batched_block_mappings = map(
      partial(_batch_block_mapping, grid_mapping.grid),
      avals_to_batch,
      all_dims[num_index_operands:],
      block_mappings,
  )

  batched_in_shapes = tuple(
      jax.ShapeDtypeStruct(x.shape if dim is batching.not_mapped else
                           tuple_insert(x.shape, dim, axis_size),
                           x.dtype)
      for x, dim in zip(in_shapes, dims))
  batched_out_shapes = tuple(
      jax.ShapeDtypeStruct(tuple_insert(x.shape, 0, axis_size), x.dtype)
      for x in out_shapes)

  batched_grid_mapping = grid_mapping.replace(
      grid=(axis_size, *grid_mapping.grid),
      block_mappings=tuple(batched_block_mappings),
      mapped_dims=(0,) + tuple(a + 1 for a in grid_mapping.mapped_dims))
  out = pallas_call_p.bind(
      *dynamic_grid_args,
      *args,
      jaxpr=jaxpr,
      name=f"batched_{name}",
      in_shapes=batched_in_shapes,
      out_shapes=batched_out_shapes,
      which_linear=which_linear,
      grid_mapping=batched_grid_mapping,
      input_output_aliases=input_output_aliases,
      debug=debug,
      interpret=interpret,
      **compiler_params,
  )
  return out, (0,) * len(out)
