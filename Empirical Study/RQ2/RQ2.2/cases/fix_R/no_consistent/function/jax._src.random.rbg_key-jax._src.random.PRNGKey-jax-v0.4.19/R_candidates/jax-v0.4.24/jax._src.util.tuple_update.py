def tuple_update(t, idx, val):
  assert 0 <= idx < len(t), (idx, len(t))
  return t[:idx] + (val,) + t[idx+1:]
