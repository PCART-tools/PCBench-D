def _update_annotation(
    f: lu.WrappedFun, orig_type: Optional[core.InputType],
    axis_size: core.AxisSize, axis_name: AxisName,
    explicit_in_dims: Sequence[Optional[Union[int, ConcatAxis]]],
    segment_lens: Sequence[Array],
  ) -> lu.WrappedFun:
  if orig_type is None: return f
  # By convention, `explicit_in_dims` only accounts for explicit arguments.
  assert len(explicit_in_dims) == sum(explicit for _, explicit in orig_type)
  # We need to:
  #  * if `axis_size` is dynamic, add a new implicit binder (type) for it;
  #  * for each element of `segment_lengths`, add a new explicit binder for it;
  #  * drop other implicit binders, replacing DBIdx which refer to them with
  #    Name objects;
  #  * for each (aval, in_dim) pair: if int-valued in_dim, add batch axis (int
  #    size if `axis_size` is int, otherwise Name); if ConcatAxis-valued in_dim,
  #    add batch axis (int if corresponding segment_lengths is concrete, Name if
  #    not);
  #  * generate full in_type with implicit args too.

  class Name:
    def __init__(self, a): self.a = a
  names = [Name(a) for a, _  in orig_type]
  avals = [a.update(shape=tuple(names[d.val] if type(d) is pe.DBIdx else d  # type: ignore
                                for d in a.shape))
           if type(a) is core.DShapedArray else a for a, e in orig_type if e]

  new_avals = [core.raise_to_shaped(core.get_aval(s)) for s in segment_lens]
  sz = Name(axis_size.aval) if isinstance(axis_size, Tracer) else axis_size
  for a, d in zip(avals, explicit_in_dims):
    if isinstance(d, ConcatAxis):
      s = segment_lens[d.segment_lengths.val]
      if isinstance(core.get_aval(s), core.ConcreteArray):
        shape = list(a.shape)  # type: ignore
        shape[d.axis] = int(s.sum())  # specialize on shape if we can
        new_avals.append(a.update(shape=tuple(shape)))
      else:
        new_avals.append(a)
    else:
      new_avals.append(core.unmapped_aval(sz, axis_name, d, a))  # type: ignore

  mentioned = {d for a in new_avals if type(a) is core.DShapedArray
               for d in a.shape if type(d) is Name}
  expl_names = set(map(Name, new_avals))
  impl_names = mentioned - expl_names  # type: ignore
  impl_part = [(n.a, False) for n in impl_names]  # type: ignore
  name_map = {n: pe.DBIdx(i) for i, n in enumerate((*impl_names, *expl_names))}
  expl_part = [(a.update(shape=tuple(name_map.get(d, d) for d in a.shape))
                if type(a) is core.DShapedArray else a, True) for a in new_avals]
  return lu.annotate(f, (*impl_part, *expl_part))
