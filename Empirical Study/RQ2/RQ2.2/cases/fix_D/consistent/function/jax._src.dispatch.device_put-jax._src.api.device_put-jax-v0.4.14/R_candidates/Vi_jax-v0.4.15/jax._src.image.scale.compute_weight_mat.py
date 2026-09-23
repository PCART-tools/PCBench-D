def compute_weight_mat(input_size: core.DimSize,
                       output_size: core.DimSize,
                       scale,
                       translation,
                       kernel: Callable,
                       antialias: bool):
  dtype = jnp.result_type(scale, translation)
  inv_scale = 1. / scale
  # When downsampling the kernel should be scaled since we want to low pass
  # filter and interpolate, but when upsampling it should not be since we only
  # want to interpolate.
  kernel_scale = jnp.maximum(inv_scale, 1.) if antialias else 1.
  sample_f = ((jnp.arange(output_size, dtype=dtype) + 0.5) * inv_scale -
              translation * inv_scale - 0.5)
  x = (
      jnp.abs(sample_f[jnp.newaxis, :] -
              jnp.arange(input_size, dtype=dtype)[:, jnp.newaxis]) /
      kernel_scale)
  weights = kernel(x)

  total_weight_sum = jnp.sum(weights, axis=0, keepdims=True)
  weights = jnp.where(
      jnp.abs(total_weight_sum) > 1000. * float(np.finfo(np.float32).eps),
      jnp.divide(weights, jnp.where(total_weight_sum != 0,  total_weight_sum, 1)),
      0)
  # Zero out weights where the sample location is completely outside the input
  # range.
  # Note sample_f has already had the 0.5 removed, hence the weird range below.
  input_size_minus_0_5 = core.dimension_as_value(input_size) - 0.5
  return jnp.where(
      jnp.logical_and(sample_f >= -0.5,
                      sample_f <= input_size_minus_0_5)[jnp.newaxis, :], weights, 0)
