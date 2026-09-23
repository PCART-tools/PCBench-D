def _swap_impl(ref: AbstractRef, value: Array, *idx: Any, tree):
  del ref, value, idx, tree
  raise ValueError("Cannot run stateful primitive.")
