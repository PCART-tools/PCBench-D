def _concatenate_dtype_rule(*operands, **kwargs):
  _check_same_dtypes('concatenate', False, *(o.dtype for o in operands))
  return operands[0].dtype
