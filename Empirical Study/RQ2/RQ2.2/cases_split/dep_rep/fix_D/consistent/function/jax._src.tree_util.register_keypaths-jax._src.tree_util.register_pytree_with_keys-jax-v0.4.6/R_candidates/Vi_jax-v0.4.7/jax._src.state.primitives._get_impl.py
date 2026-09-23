def _get_impl(ref: AbstractRef, *idx: int, **_):
  del ref, idx
  raise ValueError("Cannot run stateful primitive.")
