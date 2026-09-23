@lu.transformation_with_aux
def _flatten_jvp(primal_name, jvp_name, in_tree, maybe_out_type, *args):
  primals_in, tangents_in = split_list(args, [len(args) // 2])
  py_primals = tree_unflatten(in_tree, primals_in)
  py_tangents = tree_unflatten(in_tree, tangents_in)
  pair_out = yield (py_primals, py_tangents), {}
  if not isinstance(pair_out, (list, tuple)) or len(pair_out) != 2:
    msg = (f"Custom JVP rule {jvp_name} for function {primal_name} "
           "must produce a pair (list or tuple of length two) representing "
           f"primal and tangent outputs, but got {pair_out}.")
    raise TypeError(msg)
  py_primals_out, py_tangents_out = pair_out
  primals_out, out_tree = tree_flatten(py_primals_out)
  tangents_out, out_tree2 = tree_flatten(py_tangents_out)
  primal_avals = [core.raise_to_shaped(core.get_aval(x)) for x in primals_out]
  if out_tree != out_tree2:
    msg = (f"Custom JVP rule {jvp_name} for function {primal_name} must "
           "produce primal and tangent outputs with equal container (pytree) "
           f"structures, but got {out_tree} and {out_tree2} respectively.")
    raise TypeError(msg)
  # If the primal function already ran, check out_tree agreement.
  try: out_type_ = maybe_out_type()
  except lu.StoreException: out_type_ = None
  if out_type_ is not None:
    out_tree_, primal_avals_ = out_type_
    ty_tree  = tree_unflatten(out_tree , [a.str_short() for a in primal_avals])
    ty_tree_ = tree_unflatten(out_tree_, [a.str_short() for a in primal_avals_])
    if out_tree_ != out_tree:
      m = (f"Custom JVP rule {jvp_name} for function {primal_name} must "
           "produce a pair (list or tuple of length two) "
           "where the first element represents the primal output "
           "(equal in value to the output of the custom_jvp-decorated function "
           f"{primal_name}, "
           "and in particular of the same container/pytree structure), but "
           "instead the JVP rule output's first element had container/pytree "
           "structure:\n"
           f"""    {str(ty_tree ).replace("'", "")}\n"""
           f"while the custom_jvp-decorated function {primal_name} had output "
           "container/pytree structure:\n"
           f"""    {str(ty_tree_).replace("'", "")}.""")
      raise TypeError(m)
    if not all(map(core.typematch, primal_avals, primal_avals_)):
      m = (f"Custom JVP rule {jvp_name} for function {primal_name} must "
           "produce a pair (list or tuple of length two) "
           "where the first element represents the primal output "
           "(equal in value to the output of the custom_jvp-decorated function "
           f"{primal_name}, "
           "and in particular with leaves of the same shape/dtype), but "
           "instead the JVP rule output's first element had shapes/dtypes of:\n"
           f"""    {str(ty_tree ).replace("'", "")}\n"""
           f"while the custom_jvp-decorated function {primal_name} had output "
           "shapes/dtypes of:\n"
           f"""    {str(ty_tree_).replace("'", "")}""")
      raise TypeError(m)
  # TODO(mattjj): compare primals' tangent types to tangent objects' types
  primal_avals_out = [
      raise_to_shaped(core.get_aval(x), weak_type=False).strip_named_shape()
      for x in primals_out]
  tangent_avals_out = [
      raise_to_shaped(core.get_aval(t), weak_type=False).strip_named_shape()
      if type(t) is not SymbolicZero else t.aval for t in tangents_out]
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
  yield primals_out + tangents_out, (out_tree, primal_avals)
