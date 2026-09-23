def _split(op, ary, indices_or_sections, axis=0):
  _check_arraylike(op, ary)
  ary = asarray(ary)
  axis = core.concrete_or_error(operator.index, axis, f"in jax.numpy.{op} argument `axis`")
  size = ary.shape[axis]
  if isinstance(indices_or_sections, (tuple, list)):
    indices_or_sections = np.array(
        [core.concrete_or_error(np.int64, i_s, f"in jax.numpy.{op} argument 1")
         for i_s in indices_or_sections], np.int64)
    split_indices = np.concatenate([[np.int64(0)], indices_or_sections,
                                    [np.int64(size)]])
  elif (isinstance(indices_or_sections, (np.ndarray, ndarray)) and
        indices_or_sections.ndim > 0):
    indices_or_sections = np.array(
        [core.concrete_or_error(np.int64, i_s, f"in jax.numpy.{op} argument 1")
         for i_s in indices_or_sections], np.int64)
    split_indices = np.concatenate([[np.int64(0)], indices_or_sections,
                                    [np.int64(size)]])
  else:
    indices_or_sections = core.concrete_or_error(np.int64, indices_or_sections,
                                                 f"in jax.numpy.{op} argument 1")
    part_size, r = _divmod(size, indices_or_sections)
    if r == 0:
      split_indices = np.arange(indices_or_sections + 1,
                                dtype=np.int64) * part_size
    elif op == "array_split":
      split_indices = np.concatenate(
          [np.arange(r + 1, dtype=np.int64) * (part_size + 1),
           np.arange(indices_or_sections - r, dtype=np.int64) * part_size
           + ((r + 1) * (part_size + 1) - 1)])
    else:
      raise ValueError("array split does not result in an equal division")
  starts, ends = [0] * ndim(ary), shape(ary)
  _subval = lambda x, i, v: subvals(x, [(i, v)])
  return [lax.slice(ary, _subval(starts, axis, start), _subval(ends, axis, end))
          for start, end in zip(split_indices[:-1], split_indices[1:])]
