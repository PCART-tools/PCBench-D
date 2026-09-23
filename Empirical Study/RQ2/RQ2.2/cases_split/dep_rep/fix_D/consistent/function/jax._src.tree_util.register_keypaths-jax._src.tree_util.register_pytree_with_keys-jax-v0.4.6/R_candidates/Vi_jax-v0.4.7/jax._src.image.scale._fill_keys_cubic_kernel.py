def _fill_keys_cubic_kernel(x):
  # http://ieeexplore.ieee.org/document/1163711/
  # R. G. Keys. Cubic convolution interpolation for digital image processing.
  # IEEE Transactions on Acoustics, Speech, and Signal Processing,
  # 29(6):1153–1160, 1981.
  out = ((1.5 * x - 2.5) * x) * x + 1.
  out = jnp.where(x >= 1., ((-0.5 * x + 2.5) * x - 4.) * x + 2., out)
  return jnp.where(x >= 2., 0., out)
