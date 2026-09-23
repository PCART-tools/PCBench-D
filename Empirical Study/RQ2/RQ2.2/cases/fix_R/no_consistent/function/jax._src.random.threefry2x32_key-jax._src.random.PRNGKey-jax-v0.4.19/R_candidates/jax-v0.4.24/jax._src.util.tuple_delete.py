def tuple_delete(t, idx):
  assert 0 <= idx < len(t), (idx, len(t))
  return t[:idx] + t[idx + 1:]
