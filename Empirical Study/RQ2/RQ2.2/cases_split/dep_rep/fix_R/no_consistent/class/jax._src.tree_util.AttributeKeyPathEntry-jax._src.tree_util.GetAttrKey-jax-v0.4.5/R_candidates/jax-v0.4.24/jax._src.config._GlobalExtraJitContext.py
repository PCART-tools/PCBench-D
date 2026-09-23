class _GlobalExtraJitContext(NamedTuple):
  numpy_rank_promotion: str | None = None
  numpy_dtype_promotion: str | None = None
  default_matmul_precision: Any | None = None
  dynamic_shapes: bool = False
  random_seed_offset: int = 0
  threefry_partitionable: bool = False
  softmax_custom_jvp: bool = False
  xla_profile_version: int = 0
