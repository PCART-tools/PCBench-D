def _custom_jvp_call_jaxpr_transpose(reduce_axes, cts, *args, fun_jaxpr,
                                     jvp_jaxpr_thunk, num_consts):
  del jvp_jaxpr_thunk, num_consts
  return ad.backward_pass(
      fun_jaxpr.jaxpr, reduce_axes, False, fun_jaxpr.consts, args, cts)
