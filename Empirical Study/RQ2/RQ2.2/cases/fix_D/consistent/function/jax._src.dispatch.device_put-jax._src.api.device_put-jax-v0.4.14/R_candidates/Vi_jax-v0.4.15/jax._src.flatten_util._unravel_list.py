def _unravel_list(indices, shapes, from_dtypes, to_dtype, arr):
  arr_dtype = dtypes.dtype(arr)
  if arr_dtype != to_dtype:
    raise TypeError(f"unravel function given array of dtype {arr_dtype}, "
                    f"but expected dtype {to_dtype}")
  chunks = jnp.split(arr, indices[:-1])
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # ignore complex-to-real cast warning
    return [lax.convert_element_type(chunk.reshape(shape), dtype)
            for chunk, shape, dtype in zip(chunks, shapes, from_dtypes)]
