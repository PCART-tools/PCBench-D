def _split(op: str, ary: ArrayLike,
           indices_or_sections: int | Sequence[int] | ArrayLike,
           axis: int = 0) -> list[Array]:
  util.check_arraylike(op, ary)
  ary = asarray(ary)
  axis = core.concrete_or_error(operator.index, axis, f"in jax.numpy.{op} argument `axis`")
  size = ary.shape[axis]
  if (isinstance(indices_or_sections, (tuple, list)) or
      isinstance(indices_or_sections, (np.ndarray, Array)) and
      indices_or_sections.ndim > 0):
    indices_or_sections = [
        core.concrete_dim_or_error(i_s, f"in jax.numpy.{op} argument 1")
        for i_s in indices_or_sections]
    split_indices = [0] + list(indices_or_sections) + [size]
  else:
    if core.is_symbolic_dim(indices_or_sections):
      raise ValueError(f"jax.numpy.{op} with a symbolic number of sections is "
                       "not supported")
    num_sections: int = core.concrete_or_error(int, indices_or_sections,
                                               f"in jax.numpy.{op} argument 1")
    part_size, r = divmod(size, num_sections)
    if r == 0:
      split_indices = [i * part_size
                       for i in range(num_sections + 1)]
    elif op == "array_split":
      split_indices = (
        [i * (part_size + 1) for i in range(r + 1)] +
        [i * part_size + ((r + 1) * (part_size + 1) - 1)
         for i in range(num_sections - r)])
    else:
      raise ValueError(f"array split does not result in an equal division: rest is {r}")
  split_indices = [i if core.is_symbolic_dim(i) else np.int64(i)  # type: ignore[misc]
                   for i in split_indices]
  starts, ends = [0] * ndim(ary), shape(ary)
  _subval = lambda x, i, v: subvals(x, [(i, v)])
  return [lax.slice(ary, _subval(starts, axis, start), _subval(ends, axis, end))
          for start, end in zip(split_indices[:-1], split_indices[1:])]
