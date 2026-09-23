def store(x_ref_or_view, idx, val, *, mask=None, eviction_policy=None) -> None:
  _ = swap(x_ref_or_view, idx, val, mask=mask, eviction_policy=eviction_policy,
           _function_name="store")
