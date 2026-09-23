def _get_impl(ref: AbstractRef, *args: Any, tree):
  del ref, args, tree
  raise ValueError("Cannot run stateful primitive.")
