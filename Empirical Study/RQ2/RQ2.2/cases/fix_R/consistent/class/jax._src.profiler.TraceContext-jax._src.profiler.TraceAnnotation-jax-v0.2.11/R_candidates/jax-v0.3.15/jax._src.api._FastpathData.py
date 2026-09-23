class _FastpathData(NamedTuple):
  xla_executable: xla.XlaExecutable
  out_pytree_def: Any
  sticky_device: xc.Device
  avals: Iterable[Any]
  lazy_exprs: Iterable[Any]
  kept_var_bitvec: Iterable[bool]
