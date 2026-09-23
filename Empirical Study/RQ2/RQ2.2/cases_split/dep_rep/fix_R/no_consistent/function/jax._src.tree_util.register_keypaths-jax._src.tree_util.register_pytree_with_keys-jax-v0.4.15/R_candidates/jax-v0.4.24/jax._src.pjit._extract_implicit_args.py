def _extract_implicit_args(
  in_type: Sequence[tuple[core.AbstractValue, bool]],
  explicit_args: Sequence[Any]
) -> Sequence[core.Tracer]:
  """
  Given an input type and explicitly-passed arguments (per the user-facing API
  calling convention), extract implicit axis size arguments from shapes of
  explicit arguments (for the trace-time / jaxpr-level calling convention).
  """
  # First, using `in_type` construct a list to represent the full argument list,
  # leaving the implicit arguments as None placeholders for now.
  explicit_args_ = iter(explicit_args)
  args = [next(explicit_args_) if expl else None for _, expl in in_type]
  assert next(explicit_args_, None) is None
  del explicit_args, explicit_args_

  # Next, populate the implicit arguments using the DBIdxs in `in_type`.
  for i, (aval, explicit) in enumerate(in_type):
    if not explicit or not isinstance(aval, core.DShapedArray):
      continue  # can't populate an implicit argument
    arg = args[i]
    assert arg is not None
    for d1, d2 in zip(aval.shape, arg.aval.shape):
      if isinstance(d1, core.DBIdx):
        if args[d1.val] is None:
          args[d1.val] = d2
        assert core.same_referent(args[d1.val], d2)
  assert all(x is not None for x in args)
  return [x for x, (_, e) in zip(args, in_type) if not e]  # type: ignore
