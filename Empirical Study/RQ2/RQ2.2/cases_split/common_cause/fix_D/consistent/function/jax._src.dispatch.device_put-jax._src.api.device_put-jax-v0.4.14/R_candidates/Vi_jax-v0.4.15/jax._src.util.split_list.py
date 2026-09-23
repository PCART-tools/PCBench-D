def split_list(args: Sequence[T], ns: Sequence[int]) -> list[list[T]]:
  args = list(args)
  lists = []
  for n in ns:
    lists.append(args[:n])
    args = args[n:]
  lists.append(args)
  return lists
