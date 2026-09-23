def _slice_memref(ref: ir.Value, ref_aval: state.AbstractRef,
                  indexer: NDIndexer,
                  ref_block_shape: tuple[int | pl_core.Mapped, ...]
                  ) -> tuple[ir.Value, state.AbstractRef, tuple[int | pl_core.Mapped, ...],
                             tuple[int | pl_core.Mapped, ...]]:
  assert ref_block_shape is not None
  target_shape = indexer.get_indexer_shape()
  starts, sizes, squeeze_dims, ref_block_shape = _indexer_to_start_size(
      indexer, ref_block_shape, cast_to_index=False,
  )
  target_ref_ty = ir.MemRefType.get(
      tuple(sizes), _dtype_to_ir_type(ref_aval.dtype),
      memory_space=ref.type.memory_space)
  inner_aval = ref_aval.inner_aval
  out_aval = ref_aval.update(inner_aval=inner_aval.update(shape=target_shape))
  out = tpu.MemRefSliceOp(target_ref_ty, ref, starts).result
  if any(squeeze_dims):
    # We need to squeeze out some dimensions
    squeezed_ref_ty = ir.MemRefType.get(
        tuple(target_shape), _dtype_to_ir_type(ref_aval.dtype),
        memory_space=ref.type.memory_space)
    out = tpu.MemRefSqueezeOp(squeezed_ref_ty, out).result
  return out, out_aval, ref_block_shape
