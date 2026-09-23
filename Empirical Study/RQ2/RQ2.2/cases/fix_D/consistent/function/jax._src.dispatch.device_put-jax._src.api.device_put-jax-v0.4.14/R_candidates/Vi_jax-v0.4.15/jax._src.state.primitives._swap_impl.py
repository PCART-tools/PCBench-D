def _swap_impl(ref: AbstractRef, value: Array, *idx: int, **_):
  del ref, value, idx
  raise ValueError("Cannot run stateful primitive.")
