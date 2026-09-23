def _register_keypaths(
    ty: type[T], handler: Callable[[T], tuple[KeyEntry, ...]]
) -> None:
  def flatten_with_keys(xs):
    children, treedef = _registry[ty].to_iter(xs)
    return list(zip(handler(xs), children)), treedef
  if ty in _registry:
    _registry_with_keypaths[ty] = _RegistryWithKeypathsEntry(
        flatten_with_keys, _registry[ty].from_iter
    )
