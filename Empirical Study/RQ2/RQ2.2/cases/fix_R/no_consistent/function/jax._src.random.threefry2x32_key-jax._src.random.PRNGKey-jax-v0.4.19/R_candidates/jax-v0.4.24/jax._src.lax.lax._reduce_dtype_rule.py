def _reduce_dtype_rule(*avals, computation, jaxpr, dimensions):
  operand_avals, init_val_avals = split_list(avals, [len(avals) // 2])
  operand_dtypes = [dtypes.canonicalize_dtype(op.dtype) for op in operand_avals]
  init_val_dtypes = [dtypes.canonicalize_dtype(init.dtype) for init in init_val_avals]
  if operand_dtypes != init_val_dtypes:
    raise TypeError(
        "reduce operand dtypes should match corresponding initial value dtypes, "
        f"got operands={operand_avals} and initial_values={init_val_avals}")
  return operand_dtypes
