def _expand(dim, size, index, tiled, x):
  shape = list(x.shape)
  if tiled:
    tile_size = shape[dim]
    shape[dim] *= size
    out = lax.full(shape, lax._const(x, 0))
    return slicing.dynamic_update_slice_in_dim(out, x, index * tile_size, dim)
  else:
    shape.insert(dim, size)
    out = lax.full(shape, lax._const(x, 0))
    return slicing.dynamic_update_index_in_dim(out, x, index, dim)
