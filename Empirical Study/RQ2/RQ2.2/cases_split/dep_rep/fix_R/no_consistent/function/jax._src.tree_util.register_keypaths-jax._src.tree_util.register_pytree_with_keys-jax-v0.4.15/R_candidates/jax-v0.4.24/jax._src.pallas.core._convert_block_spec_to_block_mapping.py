def _convert_block_spec_to_block_mapping(
    in_avals: list[jax_core.ShapedArray], block_spec: BlockSpec | None,
    aval: jax_core.ShapedArray, in_tree: Any,
    ) -> BlockSpec | None:
  if block_spec is no_block_spec:
    return None
  if block_spec.index_map is None:
    compute_index = lambda *args, **kwargs: (0,) * len(aval.shape)
    block_shape = aval.shape
  else:
    compute_index = block_spec.compute_index
    block_shape = block_spec.block_shape
  block_shape = tuple(
      mapped if s is None else s for s in block_shape)
  flat_fun, _ = api_util.flatten_fun(lu.wrap_init(compute_index), in_tree)
  jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(flat_fun, in_avals)
  return BlockMapping(block_shape, jax_core.ClosedJaxpr(jaxpr, consts))
