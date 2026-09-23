def _annot_to_flat(ndim: int, mapped_axes: Iterable[int],
                 annotation: Optional[int]) -> Optional[int]:
  if annotation is None: return None
  mapped_axes_ = set(mapped_axes)
  return [i for i in range(ndim) if i not in mapped_axes_][annotation]
