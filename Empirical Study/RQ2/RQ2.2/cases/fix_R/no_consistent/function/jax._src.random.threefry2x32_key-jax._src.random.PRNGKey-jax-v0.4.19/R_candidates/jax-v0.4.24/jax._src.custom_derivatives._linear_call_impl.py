def _linear_call_impl(*args, callee, transpose, num_callee_consts,
                      num_transpose_consts, num_res):
  del transpose
  consts, _, operands_res, operands_lin = split_list(
      args, [num_callee_consts, num_transpose_consts, num_res])
  return core.eval_jaxpr(callee.jaxpr, (), *consts, *operands_res, *operands_lin)
