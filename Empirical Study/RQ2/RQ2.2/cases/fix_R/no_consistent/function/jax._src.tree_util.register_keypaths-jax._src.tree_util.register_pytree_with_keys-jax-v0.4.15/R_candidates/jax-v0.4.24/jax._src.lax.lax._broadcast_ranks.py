def _broadcast_ranks(s1, s2):
  if len(s1) > len(s2):
    s1, s2 = s2, s1
  assert len(s1) <= len(s2)
  s1_ = s2[len(s2) - len(s1):]
  if core.definitely_equal_shape(s1_, s1): return s2
  else: raise ValueError
