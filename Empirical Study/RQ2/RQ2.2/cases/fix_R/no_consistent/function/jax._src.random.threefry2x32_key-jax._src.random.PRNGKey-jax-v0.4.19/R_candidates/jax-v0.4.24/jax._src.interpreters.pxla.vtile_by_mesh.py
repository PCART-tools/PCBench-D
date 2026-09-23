def vtile_by_mesh(fun: lu.WrappedFun,
                  mesh: Mesh,
                  in_axes: Sequence[ArrayMapping],
                  out_axes: Sequence[ArrayMapping]):
  # We vectorize in reversed order, because vmap is often biased towards
  # moving the batch axis to the front, and this way of stacking transforms
  # will order the batch axes according to the mesh axis order.
  # Not strictly necessary, but seems nicer than reversing it?
  for name, size in reversed(mesh.shape.items()):
    fun = batching.vtile(fun,
                         tuple(a.get(name, None) for a in in_axes),
                         tuple(a.get(name, None) for a in out_axes),
                         tile_size=size,
                         axis_name=name,
                         main_type=SPMDBatchTrace)
  return fun
