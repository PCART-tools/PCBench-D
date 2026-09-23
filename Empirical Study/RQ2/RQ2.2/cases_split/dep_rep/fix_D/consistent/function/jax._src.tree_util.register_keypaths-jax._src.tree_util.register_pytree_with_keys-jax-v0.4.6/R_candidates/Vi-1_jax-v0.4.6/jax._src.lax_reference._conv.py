def _conv(lhs, rhs, window_strides, pads):
  view, view_axes, rhs_axes, out_axes = _conv_view(
      lhs, rhs.shape, window_strides, pads, 0.)
  return opt_einsum.contract(
      view, view_axes, rhs, rhs_axes, out_axes, use_blas=True)
