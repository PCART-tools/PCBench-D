def typematch(aval1: AbstractValue, aval2: AbstractValue) -> bool:
  """Determine whether `aval1` and `aval2` are equivalent.

  Ignores weak_type and named_shape, other than to check that an axis name isn't
  used with different sizes.
  """
  if aval1 == aval2: return True
  # unequal avals may still represent the same type, because type is represented
  # by avals at the shaped level, and because weak type tags and (for now) named
  # shape components aren't considered part of the type
  if isinstance(aval1, ShapedArray) and isinstance(aval2, ShapedArray):
    # a bonus check for whether any named axes have inconsistent sizes
    join_named_shapes(aval1.named_shape, aval2.named_shape)
  return (raise_to_shaped(aval1, weak_type=False).strip_named_shape() ==
          raise_to_shaped(aval2, weak_type=False).strip_named_shape())
