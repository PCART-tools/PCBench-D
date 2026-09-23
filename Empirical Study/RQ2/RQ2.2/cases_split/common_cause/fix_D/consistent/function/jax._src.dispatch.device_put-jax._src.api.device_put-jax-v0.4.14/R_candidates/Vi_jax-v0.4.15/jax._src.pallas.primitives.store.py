def store(x_ref, idx, val, *, mask=None, eviction_policy="") -> None:
  _ = swap(x_ref, idx, val, mask=mask, eviction_policy=eviction_policy)
