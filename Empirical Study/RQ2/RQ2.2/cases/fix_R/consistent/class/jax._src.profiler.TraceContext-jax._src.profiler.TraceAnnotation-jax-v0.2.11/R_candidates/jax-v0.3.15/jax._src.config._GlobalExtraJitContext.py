class _GlobalExtraJitContext(NamedTuple):
  numpy_rank_promotion: Optional[str] = None
  numpy_dtype_promotion: Optional[str] = None
  default_matmul_precision: Optional[Any] = None
  dynamic_shapes: bool = False
