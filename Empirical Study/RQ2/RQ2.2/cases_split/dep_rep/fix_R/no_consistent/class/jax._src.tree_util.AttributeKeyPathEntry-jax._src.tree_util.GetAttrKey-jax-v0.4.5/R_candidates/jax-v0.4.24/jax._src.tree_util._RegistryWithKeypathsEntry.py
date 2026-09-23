class _RegistryWithKeypathsEntry(NamedTuple):
  flatten_with_keys: Callable[..., Any]
  unflatten_func: Callable[..., Any]
