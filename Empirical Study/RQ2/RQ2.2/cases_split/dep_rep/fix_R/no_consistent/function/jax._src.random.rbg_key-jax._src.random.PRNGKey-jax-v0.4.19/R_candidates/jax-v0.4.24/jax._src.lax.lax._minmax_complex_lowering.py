def _minmax_complex_lowering(x, y, *, lax_cmp_pick_x):
  result_shape = broadcast_shapes(np.shape(x), np.shape(y))
  x = _maybe_broadcast(result_shape, x)
  y = _maybe_broadcast(result_shape, y)
  rx = real(x)
  ry = real(y)
  pick_x = select(eq(rx, ry), lax_cmp_pick_x(imag(x), imag(y)),
                  lax_cmp_pick_x(rx, ry))
  return select(pick_x, x, y)
