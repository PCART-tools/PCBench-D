class _AxisConcat(abc.ABC):
  """Concatenates slices, scalars and array-like objects along a given axis."""
  axis: int
  ndmin: int
  trans1d: int
  op_name: str

  def __getitem__(self, key):
    if not isinstance(key, tuple):
      key = (key,)

    params = [self.axis, self.ndmin, self.trans1d, -1]

    if isinstance(key[0], str):
      # split off the directive
      directive, *key = key  # pytype: disable=bad-unpacking
      # check two special cases: matrix directives
      if directive == "r":
        params[-1] = 0
      elif directive == "c":
        params[-1] = 1
      else:
        vec = directive.split(",")
        k = len(vec)
        if k < 4:
          vec += params[k:]
        else:
          # ignore everything after the first three comma-separated ints
          vec = vec[:3] + params[-1]
        try:
          params = list(map(int, vec))
        except ValueError as err:
          raise ValueError(
            f"could not understand directive {directive!r}"
          ) from err

    axis, ndmin, trans1d, matrix = params

    output = []
    for item in key:
      if isinstance(item, slice):
        newobj = _make_1d_grid_from_slice(item, op_name=self.op_name)
      elif isinstance(item, str):
        raise ValueError("string directive must be placed at the beginning")
      else:
        newobj = item

      newobj = array(newobj, copy=False, ndmin=ndmin)

      if trans1d != -1 and ndmin - np.ndim(item) > 0:
        shape_obj = list(range(ndmin))
        # Calculate number of left shifts, with overflow protection by mod
        num_lshifts = ndmin - abs(ndmin + trans1d + 1) % ndmin
        shape_obj = tuple(shape_obj[num_lshifts:] + shape_obj[:num_lshifts])

        newobj = transpose(newobj, shape_obj)

      output.append(newobj)

    res = concatenate(tuple(output), axis=axis)

    if matrix != -1 and res.ndim == 1:
      # insert 2nd dim at axis 0 or 1
      res = expand_dims(res, matrix)

    return res

  def __len__(self):
    return 0
