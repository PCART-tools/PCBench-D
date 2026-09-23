def _vjp_pullback_wrapper(name, cotangent_dtypes, cotangent_shapes, io_tree,
                          fun, *py_args_):
  if len(py_args_) != 1:
    msg = (f"The function returned by `jax.vjp` applied to {name} was called "
           f"with {len(py_args_)} arguments, but functions returned by "
           "`jax.vjp` must be called with a single argument corresponding to "
           f"the single value returned by {name} (even if that returned "
           "value is a tuple or other container).\n"
           "\n"
           "For example, if we have:\n"
           "\n"
           "  def f(x):\n"
           "    return (x, x)\n"
           "  _, f_vjp = jax.vjp(f, 1.0)\n"
           "\n"
           "the function `f` returns a single tuple as output, and so we call "
           "`f_vjp` with a single tuple as its argument:\n"
           "\n"
           "  x_bar, = f_vjp((2.0, 2.0))\n"
           "\n"
           "If we instead call `f_vjp(2.0, 2.0)`, with the values 'splatted "
           "out' as arguments rather than in a tuple, this error can arise.")
    raise TypeError(msg)
  py_args, = py_args_
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
