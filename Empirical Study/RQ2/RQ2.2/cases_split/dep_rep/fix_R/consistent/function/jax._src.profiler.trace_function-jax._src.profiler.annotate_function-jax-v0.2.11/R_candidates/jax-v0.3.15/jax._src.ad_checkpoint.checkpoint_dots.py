def checkpoint_dots(prim, *_, **__) -> bool:
  # Matrix multiplies are expensive, so let's save them (and nothing else).
  return prim in {jax._src.lax.lax.dot_general_p,
                  jax._src.lax.convolution.conv_general_dilated_p}
