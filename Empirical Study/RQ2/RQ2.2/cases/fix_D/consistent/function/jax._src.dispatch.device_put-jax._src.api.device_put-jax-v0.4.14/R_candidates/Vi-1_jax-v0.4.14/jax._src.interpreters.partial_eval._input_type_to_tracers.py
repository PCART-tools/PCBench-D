def _input_type_to_tracers(
    new_arg: Callable[[AbstractValue], Tracer],
    in_avals: Sequence[AbstractValue]
  )  -> Sequence[Tracer]:
  # Create input Tracers given input AbstractValues, each of which can contain
  # DeBruijn indices which refer to positions in the input argument list. That
  # is, each element `a` of `in_avals` can have DBIdx instances in its shape,
  # which must refer to positions left of `a`'s.
  in_tracers: list[Tracer] = []

  def _substitute_tracers_in_aval(a: AbstractValue) -> AbstractValue:
    if isinstance(a, DShapedArray) and any(type(d) is DBIdx for d in a.shape):
      shape = [in_tracers[d.val] if type(d) is DBIdx else d for d in a.shape]  # type: ignore
      return a.update(shape=tuple(shape))
    return a

  for a in in_avals:
    in_tracers.append(new_arg(_substitute_tracers_in_aval(a)))
  return in_tracers
