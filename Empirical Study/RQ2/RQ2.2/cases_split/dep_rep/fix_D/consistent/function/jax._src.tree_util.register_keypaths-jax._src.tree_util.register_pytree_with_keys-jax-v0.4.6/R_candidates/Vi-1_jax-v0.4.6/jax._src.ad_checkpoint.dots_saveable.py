def dots_saveable(prim, *_, **__) -> bool:
  # Matrix multiplies are expensive, so let's save them (and nothing else).
  return prim in {lax_internal.dot_general_p,
                  lax_convolution.conv_general_dilated_p}
