def _load_lowering_rule(ctx: LoweringRuleContext, *args_flat, args_tree, **_):
  ref, indexers, mask, _ = args_tree.unflatten(args_flat)
  ref_aval, indexers_avals, _, _ = args_tree.unflatten(ctx.avals_in)
  (*slice_indexers, idx) = indexers
  # Select last aval, which is the one that will be used for the load.
  (*_, idx_aval) = indexers_avals

  if mask is not None:
    raise NotImplementedError

  ref_block_shape, *_ = ctx.block_shapes
  ref, _, ref_block_shape = _index_ref(
      ref, ref_aval, ref_block_shape, slice_indexers)
  ref_type = ir.MemRefType(ref.type)
  is_smem_load = str(ref_type.memory_space) == "#tpu.memory_space<smem>"
  ref_aval, *_ = ctx.avals_in
  (aval_out,) = ctx.avals_out
  if not is_smem_load and not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")
  if any(
      (not isinstance(a, primitives.Slice) and a.shape)
      for a in idx_aval.indices
  ):
    raise ValueError("Cannot do int indexing on TPU")
  starts, sizes, _, _ = _indexer_to_start_size(
      idx, ref_block_shape, cast_to_index=True,
  )
  load_aval = jax_core.ShapedArray(sizes, dtype=ref_aval.dtype)
  if is_smem_load:
    if ctx.avals_out[0].shape:
      raise ValueError("Can only load scalars from SMEM")
    return memref.LoadOp(ref, starts).result
  else:
    load_val = vector.LoadOp(aval_to_ir_type(load_aval), ref, starts).result
  if load_aval == aval_out:
    return load_val
  vec_type = ir.VectorType.get(aval_out.shape,
                               _dtype_to_ir_type(aval_out.dtype))
  return vector.ShapeCastOp(vec_type, load_val).result
