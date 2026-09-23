def vtile(f_flat: lu.WrappedFun,
          in_axes_flat: tuple[int | None, ...],
          out_axes_flat: tuple[int | None, ...],
          tile_size: int | None,
          axis_name: AxisName,
          main_type: type[BatchTrace] = BatchTrace):
  @curry
  def tile_axis(arg, axis: int | None, tile_size):
    if axis is None:
      return arg
    shape = list(arg.shape)
    shape[axis:axis+1] = [tile_size, shape[axis] // tile_size]
    return arg.reshape(shape)

  def untile_axis(out, axis: int | None):
    if axis is None:
      return out
    shape = list(out.shape)
    shape[axis:axis+2] = [shape[axis] * shape[axis+1]]
    return out.reshape(shape)

  @lu.transformation
  def _map_to_tile(*args_flat):
    sizes = (x.shape[i] for x, i in safe_zip(args_flat, in_axes_flat) if i is not None)
    tile_size_ = tile_size or next(sizes, None)
    assert tile_size_ is not None, "No mapped arguments?"
    outputs_flat = yield map(tile_axis(tile_size=tile_size_), args_flat, in_axes_flat), {}
    yield map(untile_axis, outputs_flat, out_axes_flat)

  return _map_to_tile(batch(
      f_flat, axis_name, tile_size, in_axes_flat, out_axes_flat, main_type=main_type))
