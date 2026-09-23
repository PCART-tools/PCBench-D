class _ThreadLocalExtraJitContext(NamedTuple):
  """A namedtuple containing states to add to the cache key.

  Just in time compilation (for jit, pmap, etc) behavior is configurable through
  global and thread-local options, used in the cache key.

  The initialization, which uses both config.py and core.py is done using
  `_update_thread_local_jit_state` in core.py to prevent circular imports.
  """
  dynamic_trace_state: Any | None = None
  axis_env_state: Hashable = ()
  mesh_context_manager: Hashable = ()
  numpy_rank_promotion: str | None = None
  numpy_dtype_promotion: str | None = None
  default_matmul_precision: Any | None = None
  dynamic_shapes: bool = False
  random_seed_offset: int = 0
  threefry_partitionable: bool = False
  softmax_custom_jvp: bool = False
  xla_profile_version: int = 0
