  def __getitem__(self, key: _IndexType | tuple[_IndexType, ...]) -> Array:
    key_tup: tuple[_IndexType, ...] = key if isinstance(key, tuple) else (key,)

    params = [self.axis, self.ndmin, self.trans1d, -1]

    directive = key_tup[0]
    if isinstance(directive, str):
      key_tup = key_tup[1:]
      # check two special cases: matrix directives
      if directive == "r":
        params[-1] = 0
      elif directive == "c":
        params[-1] = 1
      else:
        vec: list[Any] = directive.split(",")
        k = len(vec)
        if k < 4:
          vec += params[k:]
        else:
          # ignore everything after the first three comma-separated ints
          vec = vec[:3] + [params[-1]]
        try:
          params = list(map(int, vec))
        except ValueError as err:
          raise ValueError(
            f"could not understand directive {directive!r}"
          ) from err

    axis, ndmin, trans1d, matrix = params

    output = []
    for item in key_tup:
      if isinstance(item, slice):
        newobj = _make_1d_grid_from_slice(item, op_name=self.op_name)
        item_ndim = 0
      elif isinstance(item, str):
        raise ValueError("string directive must be placed at the beginning")
      else:
        newobj = array(item, copy=False)
        item_ndim = newobj.ndim

      newobj = array(newobj, copy=False, ndmin=ndmin)

      if trans1d != -1 and ndmin - item_ndim > 0:
        shape_obj = tuple(range(ndmin))
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
