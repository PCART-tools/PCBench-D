def _convert_block_spec_to_block_mapping(
    in_avals: list[jax_core.ShapedArray], block_spec: BlockSpec | None,
    ) -> BlockSpec | None:
  if block_spec is _no_block_spec:
    return None
  block_shape = tuple(
      mapped if s is None else s for s in block_spec.block_shape)
  jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(block_spec.compute_index), in_avals)
  return BlockMapping(block_shape, jax_core.ClosedJaxpr(jaxpr, consts))
