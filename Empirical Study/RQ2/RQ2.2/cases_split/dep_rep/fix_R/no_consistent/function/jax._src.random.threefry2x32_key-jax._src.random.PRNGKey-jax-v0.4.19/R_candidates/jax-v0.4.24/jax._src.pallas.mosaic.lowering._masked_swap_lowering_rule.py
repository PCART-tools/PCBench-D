def _masked_swap_lowering_rule(
    ctx: LoweringRuleContext, *args_flat, args_tree, **_
):
  ref, indexers, val, mask = args_tree.unflatten(args_flat)
  ref_aval, indexers_avals, val_aval, _ = args_tree.unflatten(ctx.avals_in)
  (*slice_indexers, idx) = indexers
  (*_, idx_aval) = indexers_avals

  if mask is not None:
    raise NotImplementedError

  ref_block_shape, *_ = ctx.block_shapes
  ref, _, ref_block_shape = _index_ref(
      ref, ref_aval, ref_block_shape, slice_indexers)

  ref_type = ir.MemRefType(ref.type)
  is_smem_store = str(ref_type.memory_space) == "#tpu.memory_space<smem>"
  (aval_out,) = ctx.avals_out
  if not isinstance(val, ir.Value):
    val = ir_constant(val, mlir_type=_dtype_to_ir_type(val_aval.dtype))
  if any(
      (not isinstance(a, primitives.Slice) and a.shape)
      for a in idx_aval.indices
  ):
    raise ValueError("Cannot do int indexing on TPU")
  if not is_smem_store and not ref_block_shape:
    raise NotImplementedError(
        "Indexing into a ()-shaped Ref not yet supported on TPU.")

  starts, _, _, _ = _indexer_to_start_size(
      idx, ref_block_shape, cast_to_index=True,
  )

  if is_smem_store:
    if val_aval.shape:
      raise ValueError("Can only store scalars to SMEM")
    result = memref.LoadOp(ref, starts).result
    memref.StoreOp(val, ref, starts)
    return result
  mem_slice_shape = list(aval_out.shape)
  for i, a in enumerate(idx_aval.indices):
    if not isinstance(a, primitives.Slice):
      mem_slice_shape.insert(i, 1)
  mem_slice_shape_iter = iter(mem_slice_shape)
  mem_slice_shape = [
      1 if b is pl_core.mapped else next(mem_slice_shape_iter)
      for b in ref_block_shape
  ]
  mem_aval = aval_out.update(shape=tuple(mem_slice_shape))
  mem_aval_vec_type = ir.VectorType.get(mem_aval.shape,
                                        _dtype_to_ir_type(mem_aval.dtype))
  result = vector.LoadOp(mem_aval_vec_type, ref, starts).result
  if mem_aval != aval_out:
    # We are slicing a scalar so provided dummy 1 indices
    result_vec_type = ir.VectorType.get(aval_out.shape,
                                        _dtype_to_ir_type(aval_out.dtype))
    result = vector.ShapeCastOp(result_vec_type, result).result
    val_vec_type = ir.VectorType.get(mem_aval.shape,
                                     _dtype_to_ir_type(mem_aval.dtype))
    val = vector.ShapeCastOp(val_vec_type, val).result
  vector.StoreOp(val, ref, starts)
  return result
