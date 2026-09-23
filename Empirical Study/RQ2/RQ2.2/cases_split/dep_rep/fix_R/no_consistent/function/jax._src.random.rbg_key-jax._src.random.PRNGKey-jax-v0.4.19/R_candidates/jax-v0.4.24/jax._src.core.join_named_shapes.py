def join_named_shapes(*named_shapes):
  result = {}
  for named_shape in named_shapes:
    for name, size in named_shape.items():
      if result.setdefault(name, size) != size:
        raise TypeError(
            f"Axis name {name} used with inconsistent sizes: {result[name]} != {size}")
  return result
