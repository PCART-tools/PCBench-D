def _is_simple_reverse_slice(idx: Any) -> bool:
  return (isinstance(idx, slice) and
          idx.start is idx.stop is None and
          isinstance(idx.step, int) and idx.step == -1)
