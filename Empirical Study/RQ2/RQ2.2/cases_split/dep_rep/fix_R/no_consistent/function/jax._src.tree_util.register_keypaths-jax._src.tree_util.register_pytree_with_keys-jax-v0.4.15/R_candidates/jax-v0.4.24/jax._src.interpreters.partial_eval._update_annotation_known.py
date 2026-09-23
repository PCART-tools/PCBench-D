def _update_annotation_known(
    f: lu.WrappedFun,
    orig_type: InputType | None,
    in_knowns: list[bool]
  ) -> lu.WrappedFun:
  if orig_type is None: return f
  # orig_type might contain DBIdx, but we're tossing out some args so we have to
  # re-index. moreover some of the implicit args may not be needed anymore.
  # so we basically just re-infer the lambda input type
  if (all(e for _, e in orig_type) and
      not any(type(d) is DBIdx for a, _ in orig_type for d in a.shape
              if type(a) is DShapedArray)):
    new_type = [ty for ty, known in zip(orig_type, in_knowns) if known]
    return lu.annotate(f, tuple(new_type))

  # Replace DBIdx with names, prune down to explicit only.
  class Name:
    def __init__(self, a): self.a = a
  names = [Name(a) for a, _  in orig_type]
  avals = [a.update(shape=tuple(names[d.val] if type(d) is DBIdx else d  # type: ignore
                                for d in a.shape))
           if type(a) is DShapedArray else a for a, e in orig_type if e]
  avals = [a for a, known in zip(avals, in_knowns) if known]
  # Figure out the implicit part: names which aren't explicit and known.
  expl_names = [o for o, (_, e) in zip(names, orig_type) if e]
  expl_names = [o for o, k in zip(expl_names, in_knowns) if k]
  expl_names_ = set(expl_names)
  impl_names = {d for a in avals if type(a) is DShapedArray for d in a.shape
                if type(d) is Name and d not in expl_names_}
  impl_part = [(n.a, False) for n in impl_names]  # type: ignore
  # Figure out the explicit part: known explicit avals, replacing names w/ dbidx
  name_map = {n: DBIdx(i) for i, n in enumerate((*impl_names, *expl_names))}
  expl_part = [(a.update(shape=tuple(name_map.get(d, d) for d in a.shape))
                if type(a) is DShapedArray else a, True) for a in avals]
  return lu.annotate(f, (*impl_part, *expl_part))
