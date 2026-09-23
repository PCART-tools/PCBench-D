@lu.transformation
def hide_mapped_axes(flat_in_axes, flat_out_axes, *flat_args):
  def _squeeze_mapped_axes(arg, axes: AxisNamePos):
    for dim in sorted(axes.values(), reverse=True):
      arg = arg.squeeze(dim)
    return arg

  def _unsqueeze_mapped_axes(out, axes: AxisNamePos):
    try:
      return jnp.expand_dims(out, tuple(axes.values()))
    except ValueError as e:
      # Improve the axis out of bounds errors
      # TODO(apaszke): Handle negative indices. Check for overlap too!
      if e.args[0].startswith('axis') and 'out of bounds' in e.args[0]:
        raise ValueError(f"One of xmap outputs has an out_axes specification of "
                         f"{axes.user_repr}, which requires the result of the xmapped "
                         f"function to have at least {max(axes.values()) - len(axes) + 1} "
                         f"positional dimensions, but it only has {out.ndim}")
      raise

  squeezed_args = map(_squeeze_mapped_axes, flat_args, flat_in_axes)
  flat_outputs = yield squeezed_args, {}
  yield map(_unsqueeze_mapped_axes, flat_outputs, flat_out_axes)
