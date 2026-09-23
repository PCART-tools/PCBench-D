def _get_impl(ref: Ref, *idx: int):
  del ref, idx
  raise ValueError("Can't evaluate `get` outside a stateful context.")
