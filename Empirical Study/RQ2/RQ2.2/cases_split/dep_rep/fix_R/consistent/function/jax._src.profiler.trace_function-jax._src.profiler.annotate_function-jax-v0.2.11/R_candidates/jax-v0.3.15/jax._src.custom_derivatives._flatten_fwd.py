@lu.transformation_with_aux
def _flatten_fwd(in_tree, *args):
  py_args = tree_unflatten(in_tree, args)
  pair_out = yield py_args, {}
  if not isinstance(pair_out, (list, tuple)) or len(pair_out) != 2:
    msg = ("Custom VJP fwd function must produce a pair (list or tuple of "
           "length two) representing primal outputs and residuals (values "
           "stored from the forward pass for use on the backward pass), "
           "got {}.")
    raise TypeError(msg.format(pair_out))
  py_outs, res = pair_out
  out, out_tree = tree_flatten(py_outs)
  res, res_tree = tree_flatten(res)
  yield res + out, (out_tree, res_tree)
