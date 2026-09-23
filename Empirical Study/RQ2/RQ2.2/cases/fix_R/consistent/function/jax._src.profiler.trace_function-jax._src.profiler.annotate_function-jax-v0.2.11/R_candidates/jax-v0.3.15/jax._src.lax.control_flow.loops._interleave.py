def _interleave(a, b, axis):
  """Given two Tensors of static shape, interleave them along the first axis."""
  assert a.shape[axis] == b.shape[axis] or a.shape[axis] == b.shape[axis] + 1
  a_pad = [(0, 0, 0)] * a.ndim
  b_pad = [(0, 0, 0)] * b.ndim
  a_pad[axis] = (0, 1 if a.shape[axis] == b.shape[axis] else 0, 1)
  b_pad[axis] = (1, 0 if a.shape[axis] == b.shape[axis] else 1, 1)
  op = lax.bitwise_or if a.dtype == np.bool_ else lax.add
  return op(lax.pad(a, lax._const(a, 0), a_pad),
            lax.pad(b, lax._const(b, 0), b_pad))
