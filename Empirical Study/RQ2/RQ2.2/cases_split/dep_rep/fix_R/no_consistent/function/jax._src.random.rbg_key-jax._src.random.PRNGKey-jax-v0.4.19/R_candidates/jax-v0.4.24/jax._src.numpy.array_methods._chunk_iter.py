def _chunk_iter(x, size):
  if size > x.shape[0]:
    yield x
  else:
    num_chunks, tail = ufuncs.divmod(x.shape[0], size)
    for i in range(num_chunks):
      yield lax.dynamic_slice_in_dim(x, i * size, size)
    if tail:
      yield lax.dynamic_slice_in_dim(x, num_chunks * size, tail)
