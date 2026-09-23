def make_transpose_from_thunk(thunk, lin_tree):
  transpose_jaxpr, transpose_consts = thunk()
  transpose_jaxpr = core.ClosedJaxpr(
      pe.convert_constvars_jaxpr(transpose_jaxpr), ())
  def transpose(res_arg, ct_out):
    args_flat = tree_leaves((res_arg, ct_out))
    ct_ins = core.jaxpr_as_fun(transpose_jaxpr)(*transpose_consts, *args_flat)
    return tree_unflatten(lin_tree, ct_ins)
  return transpose
