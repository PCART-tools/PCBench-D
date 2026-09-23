def _eval_index_map(
    ctx: TritonModuleContext, idx, block_mapping: BlockMapping | None
):
  if block_mapping is None:
    return None
  block_indices = tuple(
      lower_jaxpr_to_triton_ir(
          ctx, block_mapping.index_map_jaxpr.jaxpr, None, *idx
      )
  )
  return tuple(
      i
      if b is pallas_core.mapped
      else tc.semantic.mul(i, tc._to_tensor(b, i.dtype))
      for i, b in zip(block_indices, block_mapping.block_shape)
  )
