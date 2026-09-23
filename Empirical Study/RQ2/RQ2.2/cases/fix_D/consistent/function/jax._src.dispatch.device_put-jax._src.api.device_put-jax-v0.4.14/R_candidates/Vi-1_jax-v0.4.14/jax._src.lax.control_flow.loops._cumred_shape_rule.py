def _cumred_shape_rule(x, *, axis: int, reverse: bool):
  if axis < 0 or axis >= x.ndim:
    raise ValueError(
        f"axis {axis} is out of bounds for array of shape {x.shape}")
  return x.shape
