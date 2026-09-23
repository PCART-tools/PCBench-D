def _addupdate_impl(ref: AbstractRef, value: Array, *args: Any, tree):
  del ref, value, args, tree
  raise ValueError("Can't evaluate `addupdate` outside a stateful context.")
