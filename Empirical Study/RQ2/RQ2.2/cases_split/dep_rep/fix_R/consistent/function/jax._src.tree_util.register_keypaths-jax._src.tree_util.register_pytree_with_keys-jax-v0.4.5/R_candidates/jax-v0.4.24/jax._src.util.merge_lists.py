def merge_lists(bs: Sequence[bool], l0: Sequence[T], l1: Sequence[T]) -> list[T]:
  assert sum(bs) == len(l1) and len(bs) - sum(bs) == len(l0)
  i0, i1 = iter(l0), iter(l1)
  out = [next(i1) if b else next(i0) for b in bs]
  sentinel = object()
  assert next(i0, sentinel) is next(i1, sentinel) is sentinel
  return out
