class DebugInfo(NamedTuple):
  func_src_info: str | None  # f'{fun.__name__} at {filename}:{lineno}'
  signature: inspect.Signature | None  # inspect.signature(fun)
  in_tree: PyTreeDef | None  # caller/constructor might not have this info
  out_tree: Callable[[], PyTreeDef] | None  # lazy, not avail at trace time
  has_kwargs: bool  # whether in_tree corresponds to (args, kwargs) or args
  traced_for: str  # "jit", "scan", "make_jaxpr", etc
