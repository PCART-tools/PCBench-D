def _batch_block_mapping(grid: Tuple[int, ...], aval: jax_core.ShapedArray,
                         dim: int | batching.NotMapped,
                         block_mapping: BlockMapping | None) -> BlockMapping:
  def _block_map_function(new_idx, *args):
    if block_mapping is None:
      indices = [0] * len(aval.shape)
    else:
      indices = jax_core.eval_jaxpr(block_mapping.index_map_jaxpr.jaxpr,
                                    block_mapping.index_map_jaxpr.consts,
                                    *args)
    if dim is not batching.not_mapped:
      indices.insert(dim, new_idx)
    return tuple(indices)
  i32_aval = jax_core.ShapedArray((), jnp.int32)
  if block_mapping is None:
    idx_avals = [i32_aval] * (len(grid) + 1)
  else:
    idx_avals = [i32_aval, *block_mapping.index_map_jaxpr.in_avals]
  block_mapping_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(_block_map_function), idx_avals)
  shape = aval.shape if block_mapping is None else block_mapping.block_shape
  if dim is batching.not_mapped:
    new_block_shape = shape
  else:
    new_block_shape = tuple_insert(shape, dim, pallas_core.mapped)
  jaxpr = jax_core.ClosedJaxpr(block_mapping_jaxpr, consts)
  if block_mapping is None:
    return BlockMapping(block_shape=new_block_shape, index_map_jaxpr=jaxpr)
  return block_mapping.replace(block_shape=new_block_shape,
                               index_map_jaxpr=jaxpr)
