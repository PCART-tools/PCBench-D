def atomic_cas(ref, cmp, val):
  return atomic_cas_p.bind(ref, cmp, val)
