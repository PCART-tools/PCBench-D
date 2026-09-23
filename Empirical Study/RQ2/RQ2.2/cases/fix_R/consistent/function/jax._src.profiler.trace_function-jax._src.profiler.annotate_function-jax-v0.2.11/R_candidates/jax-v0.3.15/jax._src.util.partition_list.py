def partition_list(bs: Sequence[bool], l: Sequence[T]) -> Tuple[List[T], List[T]]:
  assert len(bs) == len(l)
  lists = [], []  # type: ignore
  for b, x in zip(bs, l):
    lists[b].append(x)
  return lists
