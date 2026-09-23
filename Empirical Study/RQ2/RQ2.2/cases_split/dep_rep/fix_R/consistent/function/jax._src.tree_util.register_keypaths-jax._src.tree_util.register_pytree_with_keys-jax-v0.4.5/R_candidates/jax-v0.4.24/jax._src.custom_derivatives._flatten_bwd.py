@lu.transformation
def _flatten_bwd(in_tree, in_avals, out_trees, *args):
  out_tree, res_tree = out_trees()
  assert len(args) == res_tree.num_leaves + out_tree.num_leaves
  res, cts_out = split_list(args, [res_tree.num_leaves])
  py_res = tree_unflatten(res_tree, res)
  py_cts_out = tree_unflatten(out_tree, cts_out)
  py_cts_in = yield (py_res, py_cts_out), {}
  # For each None in py_cts_in, indicating an argument for which the rule
  # produces no cotangent, we replace it with a pytree with the structure of the
  # corresponding subtree of in_tree and with leaves of a non-pytree sentinel
  # object, to be replaced with Nones in the final returned result.
  zero = object()  # non-pytree sentinel to replace Nones in py_cts_in
  dummy = tree_unflatten(in_tree, [object()] * in_tree.num_leaves)
  cts_in_flat = []
  append = lambda x, d: cts_in_flat.extend([x] * len(tree_flatten(d)[0])) or x
  try:
    if not isinstance(py_cts_in, tuple):
      raise ValueError
    tree_map(append,
             tuple(zero if ct is None else ct for ct in py_cts_in), dummy)
  except ValueError:
    _, in_tree2 = tree_flatten(py_cts_in)
    msg = ("Custom VJP rule must produce an output with the same container "
           "(pytree) structure as the args tuple of the primal function, "
           "and in particular must produce a tuple of length equal to the "
           "number of arguments to the primal function, but got VJP output "
           "structure {} for primal input structure {}.")
    raise TypeError(msg.format(in_tree2, in_tree)) from None
  # Ignore any None cotangents, and any corresponding to inputs for which the
  # type doesn't equal the tangent type (i.e. float0s)
  # TODO(mattjj): change this to check if tangent type represents 0dim vspace
  yield [Zero(a.at_least_vspace()) if ct is zero or a != a.at_least_vspace()
         else ct for a, ct in zip(in_avals, cts_in_flat)]
