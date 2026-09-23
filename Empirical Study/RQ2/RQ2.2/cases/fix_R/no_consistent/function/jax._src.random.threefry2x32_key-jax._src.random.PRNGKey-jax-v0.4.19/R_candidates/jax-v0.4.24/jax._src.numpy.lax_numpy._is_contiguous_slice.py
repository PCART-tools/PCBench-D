def _is_contiguous_slice(idx):
  return (isinstance(idx, slice) and
          (idx.start is None or _is_integer_index(idx.start)) and
          (idx.stop is None or _is_integer_index(idx.stop)) and
          (idx.step is None or (_is_integer_index(idx.step) and idx.step == 1)))
