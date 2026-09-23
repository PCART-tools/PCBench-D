@lu.transformation_with_aux
def _flatten_fwd(primal_name, fwd_name, in_tree, maybe_out_type, *args):
  py_args = tree_unflatten(in_tree, args)
  pair_out = yield py_args, {}
  if not isinstance(pair_out, (list, tuple)) or len(pair_out) != 2:
    msg = (f"Custom VJP fwd rule {fwd_name} for function {primal_name} "
           "must produce a pair (list or tuple of length two) where the first "
           "element represents the primal output (equal to those of the "
           f"custom_vjp-decorated function {primal_name}) and the "
           "second element represents residuals (i.e. values stored from the "
           "forward pass for use on the backward pass), but "
           f"instead of a pair the fwd rule {fwd_name} produced {pair_out}.")
    raise TypeError(msg)
  py_primals_out, res = pair_out
  primals_out, out_tree = tree_flatten(py_primals_out)
  res, res_tree = tree_flatten(res)
  primal_avals = [core.raise_to_shaped(core.get_aval(x)) for x in primals_out]
  # If the primal function already ran, check out_tree agreement.
  try: out_type_ = maybe_out_type()
  except lu.StoreException: out_type_ = None
  if out_type_ is not None:
    out_tree_, primal_avals_ = out_type_
    ty_tree  = tree_unflatten(out_tree , [a.str_short() for a in primal_avals])
    ty_tree_ = tree_unflatten(out_tree_, [a.str_short() for a in primal_avals_])
    if out_tree_ != out_tree:
      m = (f"Custom VJP fwd rule {fwd_name} for function {primal_name} "
           "must produce a pair (list or tuple of length two) where the first "
           "element represents the primal output "
           "(equal to the output of the custom_vjp-decorated function "
           f"{primal_name}) and the "
           "second element represents residuals (i.e. values stored from the "
           "forward pass for use on the backward pass), but "
           "instead the fwd rule output's first element had container/pytree "
           "structure:\n"
           f"""    {str(ty_tree ).replace("'", "")}\n"""
           f"while the custom_vjp-decorated function {primal_name} had output "
           "container/pytree structure:\n"
           f"""    {str(ty_tree_).replace("'", "")}.""")
      raise TypeError(m)
    if not all(map(core.typematch, primal_avals, primal_avals_)):
      m = (f"Custom VJP fwd rule {fwd_name} for function {primal_name} must "
           "produce a pair (list or tuple of length two) "
           "where the first element represents the primal output "
           "(equal to the output of the custom_vjp-decorated function "
           f"{primal_name}) and the second element represents residuals "
           "(i.e. values stored from the forward pass for use on the "
           "backward pass), but "
           "instead the fwd rule output's first element had shapes/dtypes of:\n"
           f"""    {str(ty_tree ).replace("'", "")}\n"""
           f"while the custom_vjp-decorated function {primal_name} had output "
           "shapes/dtypes of:\n"
           f"""    {str(ty_tree_).replace("'", "")}""")
      raise TypeError(m)
  yield (*res, *primals_out), (out_tree, res_tree)
