def _compute_fans(shape: core.NamedShape, in_axis=-2, out_axis=-1,
                  batch_axis=()):
  """
  Compute effective input and output sizes for a linear or convolutional layer.

  Axes not in in_axis, out_axis, or batch_axis are assumed to constitute the
  "receptive field" of a convolution (kernel spatial dimensions).
  """
  if isinstance(in_axis, int):
    in_size = shape[in_axis]
  else:
    in_size = int(np.prod([shape[i] for i in in_axis]))
  if isinstance(out_axis, int):
    out_size = shape[out_axis]
  else:
    out_size = int(np.prod([shape[i] for i in out_axis]))
  if isinstance(batch_axis, int):
    batch_size = shape[batch_axis]
  else:
    batch_size = int(np.prod([shape[i] for i in batch_axis]))
  receptive_field_size = shape.total / in_size / out_size / batch_size
  fan_in = in_size * receptive_field_size
  fan_out = out_size * receptive_field_size
  return fan_in, fan_out
