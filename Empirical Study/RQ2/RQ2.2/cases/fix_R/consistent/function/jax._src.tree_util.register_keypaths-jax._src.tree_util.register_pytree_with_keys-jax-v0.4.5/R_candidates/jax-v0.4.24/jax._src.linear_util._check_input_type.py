def _check_input_type(in_type: core.InputType) -> None:
  # Check that in_type is syntactically well-formed
  assert type(in_type) is tuple and all(type(e) is tuple for e in in_type)
  assert all(isinstance(a, core.AbstractValue) and type(b) is bool
             and not isinstance(a, core.ConcreteArray) for a, b in in_type)

  def valid_size(d) -> bool:
    if isinstance(d, core.DBIdx) and type(d.val) is int and d.val >= 0:
      return True
    return (isinstance(d, (int, core.DBIdx, core.DArray)) and
            (not isinstance(d, core.DArray) or type(d) is core.bint and not d.shape))
  assert all(valid_size(d) for a, _ in in_type if type(a) is core.DShapedArray
             for d in a.shape)

  # Check that all DBIdx point to positions to the left of the input on which
  # they appear.
  assert all(d.val < i for i, (aval, _) in enumerate(in_type)
             if isinstance(aval, core.DShapedArray) for d in aval.shape
             if isinstance(d, core.DBIdx))

  # Check that all implicit arguments have at least one DBIdx pointing to them.
  provided = [e for _, e in in_type]
  for aval, _ in in_type:
    if type(aval) is core.DShapedArray:
      for d in aval.shape:
        if isinstance(d, core.DBIdx):
          provided[d.val] = True
  assert all(provided)
