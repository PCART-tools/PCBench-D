def sort_key_val(keys, values, dimension=-1):
  idxs = list(np.ix_(*[np.arange(d) for d in keys.shape]))
  idxs[dimension] = np.argsort(keys, axis=dimension)
  return keys[tuple(idxs)], values[tuple(idxs)]
