def _split(op: str, ary: ArrayLike,
           indices_or_sections: Union[int, Sequence[int], ArrayLike],
           axis: int = 0) -> list[Array]:
  util.check_arraylike(op, ary)
  ary = asarray(ary)
  axis = core.concrete_or_error(operator.index, axis, f"in jax.numpy.{op} argument `axis`")
  size = ary.shape[axis]
  if isinstance(indices_or_sections, (tuple, list)):
    indices_or_sections = np.array(
        [core.concrete_or_error(np.int64, i_s, f"in jax.numpy.{op} argument 1")
         for i_s in indices_or_sections], np.int64)
    split_indices = np.concatenate([[np.int64(0)], indices_or_sections,
                                    [np.int64(size)]])
  elif (isinstance(indices_or_sections, (np.ndarray, Array)) and
        indices_or_sections.ndim > 0):
    indices_or_sections = np.array(
        [core.concrete_or_error(np.int64, i_s, f"in jax.numpy.{op} argument 1")
         for i_s in indices_or_sections], np.int64)
    split_indices = np.concatenate([[np.int64(0)], indices_or_sections,
                                    [np.int64(size)]])
  else:
    num_sections: int = core.concrete_or_error(int, indices_or_sections,
                                               f"in jax.numpy.{op} argument 1")
    part_size, r = divmod(size, num_sections)
    if r == 0:
      split_indices = np.array([np.int64(i) * part_size
                                for i in range(num_sections + 1)])
    elif op == "array_split":
      split_indices = np.array(
        [np.int64(i) * (part_size + 1) for i in range(r + 1)] +
        [np.int64(i) * part_size + ((r + 1) * (part_size + 1) - 1)
         for i in range(num_sections - r)])
    else:
      raise ValueError("array split does not result in an equal division")
  starts, ends = [0] * ndim(ary), shape(ary)
  _subval = lambda x, i, v: subvals(x, [(i, v)])
  return [lax.slice(ary, _subval(starts, axis, start), _subval(ends, axis, end))
          for start, end in zip(split_indices[:-1], split_indices[1:])]
