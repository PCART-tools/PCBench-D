def _allreduce_abstract_eval(*args, axes, axis_index_groups):
  # TODO(frostig,mattjj,jekbradbury): maybe check aval names here
  pos_axes = tuple(axis for axis in axes if isinstance(axis, int))
  named_shapes = [arg.named_shape for arg in args]
  if axis_index_groups is None:
    named_axes = {axis for axis in axes if not isinstance(axis, int)}
    named_shapes = [{name: size for name, size in arg.named_shape.items()
                     if name not in named_axes} for arg in args]
  else:
    if len(pos_axes) != 0:
      raise ValueError(f"axis_index_groups can only be used with reductions over "
                       f"named axes, but got: {axes}")
  return [ShapedArray(lax._reduce_op_shape_rule(raise_to_shaped(arg), axes=pos_axes),
                      arg.dtype, named_shape=named_shape)
          for arg, named_shape in zip(args, named_shapes)]
