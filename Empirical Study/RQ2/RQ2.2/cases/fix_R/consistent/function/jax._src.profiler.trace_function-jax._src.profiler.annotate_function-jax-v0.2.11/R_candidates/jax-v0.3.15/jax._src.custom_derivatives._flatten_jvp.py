@lu.transformation_with_aux
def _flatten_jvp(in_tree, *args):
  primals_in, tangents_in = split_list(args, [len(args) // 2])
  py_primals = tree_unflatten(in_tree, primals_in)
  py_tangents = tree_unflatten(in_tree, tangents_in)
  pair_out = yield (py_primals, py_tangents), {}
  if not isinstance(pair_out, (list, tuple)) or len(pair_out) != 2:
    msg = ("Custom JVP rule must produce a pair (list or tuple of length two) "
           "representing primal and tangent outputs, got {}.")
    raise TypeError(msg.format(pair_out))
  py_primals_out, py_tangents_out = pair_out
  primals_out, out_tree = tree_flatten(py_primals_out)
  tangents_out, out_tree2 = tree_flatten(py_tangents_out)
  if out_tree != out_tree2:
    msg = ("Custom JVP rule must produce primal and tangent outputs with equal "
           "container (pytree) structures, but got {} and {} respectively.")
    raise TypeError(msg.format(out_tree, out_tree2))
  # TODO(mattjj): compare primals' tangent types to tangent objects' types
  primal_avals_out = [
      raise_to_shaped(core.get_aval(x), weak_type=False).strip_named_shape()
      for x in primals_out]
  tangent_avals_out = [
      raise_to_shaped(core.get_aval(t), weak_type=False).strip_named_shape()
      for t in tangents_out]
  if primal_avals_out != tangent_avals_out:
    if len(primal_avals_out) == 1:
      (av1,), (av2,) = primal_avals_out, tangent_avals_out
      msg = ("Custom JVP rule must produce primal and tangent outputs with "
             "equal shapes and dtypes, but got {} and {} respectively.")
      raise TypeError(msg.format(av1.str_short(), av2.str_short()))
    else:
      msg = ("Custom JVP rule must produce primal and tangent outputs with "
             "equal shapes and dtypes, but got:\n{}")
      disagreements = (
          f"  primal {av1.str_short()} for tangent {av2.str_short()}"
          for av1, av2 in zip(primal_avals_out, tangent_avals_out) if av1 != av2)
      raise TypeError(msg.format('\n'.join(disagreements)))
  yield primals_out + tangents_out, out_tree
