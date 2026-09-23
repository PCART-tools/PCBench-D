def _unravel_list_single_dtype(indices, shapes, arr):
  chunks = jnp.split(arr, indices[:-1])
  return [chunk.reshape(shape) for chunk, shape in zip(chunks, shapes)]
