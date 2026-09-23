def _moveaxis(ndim: int, shard_axes: Dict[core.AxisName, int],
              src: int, dst: int) -> Dict[core.AxisName, int]:
  lst: List[Optional[core.AxisName]] = [None] * ndim
  for k, v in shard_axes.items():
    lst[v] = k
  name = lst.pop(src)
  lst.insert(dst - (src < dst), name)
  return {name: i for i, name in enumerate(lst) if name is not None}
