def _vjp_pullback_wrapper(cotangent_dtypes, cotangent_shapes,
                          io_tree, fun, py_args):
  in_tree_expected, out_tree = io_tree
  args, in_tree = tree_flatten(py_args)
  if in_tree != in_tree_expected:
    raise TypeError(f"Tree structure of cotangent input {in_tree}, does not match structure of "
                    f"primal output {in_tree_expected}.")
  for arg, ct_dtype, ct_shape in safe_zip(args, cotangent_dtypes, cotangent_shapes):
    expected_tangent_dtype = core.primal_dtype_to_tangent_dtype(_dtype(arg))
    if expected_tangent_dtype != ct_dtype:
      raise TypeError(
          f"Type of cotangent input to vjp pullback function ({ct_dtype}) is not "
          f"the expected tangent type ({expected_tangent_dtype}) of corresponding primal output "
          f"with dtype {_dtype(arg)}.")
    if np.shape(arg) != ct_shape:
      raise ValueError(
          f"Shape of cotangent input to vjp pullback function {np.shape(arg)} "
          "must be the same as the shape of corresponding primal input "
          f"{ct_shape}.")
  ans = fun(*args)
  return tree_unflatten(out_tree, ans)
