class _ThreadLocalExtraJitContext(NamedTuple):
  """"A namedtuple containing states to add to the cache key.

  Just in time compilation (for jit, pmap, etc) behavior is configurable through
  global and thread-local options, used in the cache key.

  The initialization, which uses both config.py and core.py is done using
  `_update_thread_local_jit_state` in core.py to prevent circular imports.
  """
  dynamic_trace_state: Optional[Any] = None
  axis_env_state: Optional[Hashable] = None
  numpy_rank_promotion: Optional[str] = None
  numpy_dtype_promotion: Optional[str] = None
  default_matmul_precision: Optional[Any] = None
  dynamic_shapes: bool = False
