def _moveaxis(ndim: int, shard_axes: dict[core.AxisName, int],
              src: int, dst: int) -> dict[core.AxisName, int]:
  lst: list[core.AxisName | None] = [None] * ndim
  for k, v in shard_axes.items():
    lst[v] = k
  name = lst.pop(src)
  lst.insert(dst - (src < dst), name)
  return {name: i for i, name in enumerate(lst) if name is not None}
