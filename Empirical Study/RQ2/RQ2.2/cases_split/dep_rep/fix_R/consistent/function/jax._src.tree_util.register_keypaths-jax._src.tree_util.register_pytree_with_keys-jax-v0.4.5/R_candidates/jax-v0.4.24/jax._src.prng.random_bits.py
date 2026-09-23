def random_bits(keys, bit_width, shape):
  shape = core.as_named_shape(shape)
  for name, size in shape.named_items:
    # TODO(frostig,mattjj,apaszke): Is this real_size check necessary,
    # and is it meant to raise a user-facing ValueError? Should it be
    # an `assert` (or RuntimeError) instead? Why do we check it in
    # calls to `random_bits` instead of a more common paralleism path?
    real_size = lax.psum(1, name)
    if real_size != size:
      raise ValueError(f"The shape of axis {name} was specified as {size}, "
                       f"but it really is {real_size}")
    axis_index = lax.axis_index(name)
    keys = random_fold_in(keys, axis_index)
  return random_bits_p.bind(keys, bit_width=bit_width, shape=shape.positional)
