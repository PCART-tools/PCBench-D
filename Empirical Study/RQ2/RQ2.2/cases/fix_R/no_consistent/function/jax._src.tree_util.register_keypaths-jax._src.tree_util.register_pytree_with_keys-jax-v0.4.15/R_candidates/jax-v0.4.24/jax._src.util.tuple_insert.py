def tuple_insert(t, idx, val):
  assert 0 <= idx <= len(t), (idx, len(t))
  return t[:idx] + (val,) + t[idx:]
