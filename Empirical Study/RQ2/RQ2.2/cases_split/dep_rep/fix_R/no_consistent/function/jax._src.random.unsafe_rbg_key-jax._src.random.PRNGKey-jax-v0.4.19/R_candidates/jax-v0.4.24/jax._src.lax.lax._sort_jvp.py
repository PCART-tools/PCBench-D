def _sort_jvp(primals, tangents, *, dimension, is_stable, num_keys):
  shape = primals[0].shape
  iotas = []
  for dim, size in enumerate(shape):
    dtype = np.int32 if size < np.iinfo(np.int32).max else np.int64
    iotas.append(broadcasted_iota(dtype, shape, dim))
  primals = sort_p.bind(*(primals + (iotas[dimension],)), dimension=dimension,
                        is_stable=is_stable, num_keys=num_keys)
  idx = tuple(primals[-1] if i == dimension else iotas[i]
              for i in range(len(shape)))
  tangents_out = tuple(t if type(t) is ad_util.Zero else t[idx] for t in tangents)
  return tuple(primals[:-1]), tangents_out
