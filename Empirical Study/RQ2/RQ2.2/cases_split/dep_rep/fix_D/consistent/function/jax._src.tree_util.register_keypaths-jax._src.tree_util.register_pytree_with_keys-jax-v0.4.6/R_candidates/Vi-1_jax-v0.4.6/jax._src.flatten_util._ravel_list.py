def _ravel_list(lst):
  if not lst: return jnp.array([], jnp.float32), lambda _: []
  from_dtypes = [dtypes.dtype(l) for l in lst]
  to_dtype = dtypes.result_type(*from_dtypes)
  sizes, shapes = unzip2((jnp.size(x), jnp.shape(x)) for x in lst)
  indices = np.cumsum(sizes)

  if all(dt == to_dtype for dt in from_dtypes):
    # Skip any dtype conversion, resulting in a dtype-polymorphic `unravel`.
    # See https://github.com/google/jax/issues/7809.
    del from_dtypes, to_dtype
    def unravel(arr):
      chunks = jnp.split(arr, indices[:-1])
      return [chunk.reshape(shape) for chunk, shape in zip(chunks, shapes)]
    raveled = jnp.concatenate([jnp.ravel(e) for e in lst])
    return raveled, unravel

  # When there is more than one distinct input dtype, we perform type
  # conversions and produce a dtype-specific unravel function.
  def unravel(arr):
    arr_dtype = dtypes.dtype(arr)
    if arr_dtype != to_dtype:
      raise TypeError(f"unravel function given array of dtype {arr_dtype}, "
                      f"but expected dtype {to_dtype}")
    chunks = jnp.split(arr, indices[:-1])
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")  # ignore complex-to-real cast warning
      return [lax.convert_element_type(chunk.reshape(shape), dtype)
              for chunk, shape, dtype in zip(chunks, shapes, from_dtypes)]

  ravel = lambda e: jnp.ravel(lax.convert_element_type(e, to_dtype))
  raveled = jnp.concatenate([ravel(e) for e in lst])
  return raveled, unravel
