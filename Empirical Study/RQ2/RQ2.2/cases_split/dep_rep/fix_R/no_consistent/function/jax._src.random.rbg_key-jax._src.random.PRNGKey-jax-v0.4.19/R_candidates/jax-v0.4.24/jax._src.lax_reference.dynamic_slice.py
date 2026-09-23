def dynamic_slice(operand, start_indices, slice_sizes):
  out = np.zeros(slice_sizes, dtype=operand.dtype)
  idx = tuple(_slice(start, start+size)
              for start, size in zip(start_indices, slice_sizes))
  section = operand[idx]
  out[tuple(_slice(None, stop) for stop in section.shape)] = section
  return out
