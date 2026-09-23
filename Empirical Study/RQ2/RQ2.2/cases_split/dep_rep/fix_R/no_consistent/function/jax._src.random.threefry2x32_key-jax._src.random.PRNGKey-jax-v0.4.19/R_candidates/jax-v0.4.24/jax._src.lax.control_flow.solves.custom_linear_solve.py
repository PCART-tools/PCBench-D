@api_boundary
def custom_linear_solve(
    matvec, b, solve, transpose_solve=None, symmetric=False, has_aux=False):
  """Perform a matrix-free linear solve with implicitly defined gradients.

  This function allows for overriding or defining gradients for a linear
  solve directly via implicit differentiation at the solution, rather than by
  differentiating *through* the solve operation. This can sometimes be much faster
  or more numerically stable, or differentiating through the solve operation
  may not even be implemented (e.g., if ``solve`` uses ``lax.while_loop``).

  Required invariant::

      x = solve(matvec, b)  # solve the linear equation
      assert matvec(x) == b  # not checked

  Args:
    matvec: linear function to invert. Must be differentiable.
    b: constant right handle side of the equation. May be any nested structure
      of arrays.
    solve: higher level function that solves for solution to the linear
      equation, i.e., ``solve(matvec, x) == x`` for all ``x`` of the same form
      as ``b``. This function need not be differentiable.
    transpose_solve: higher level function for solving the transpose linear
      equation, i.e., ``transpose_solve(vecmat, x) == x``, where ``vecmat`` is
      the transpose of the linear map ``matvec`` (computed automatically with
      autodiff). Required for backwards mode automatic differentiation, unless
      ``symmetric=True``, in which case ``solve`` provides the default value.
    symmetric: bool indicating if it is safe to assume the linear map
      corresponds to a symmetric matrix, i.e., ``matvec == vecmat``.
    has_aux: bool indicating whether the ``solve`` and ``transpose_solve`` functions
      return auxiliary data like solver diagnostics as a second argument.

  Returns:
    Result of ``solve(matvec, b)``, with gradients defined assuming that the
      solution ``x`` satisfies the linear equation ``matvec(x) == b``.
  """
  if transpose_solve is None and symmetric:
    transpose_solve = solve

  b_flat, in_args_tree = tree_flatten((b,))
  b_avals = tuple(_map(_abstractify, b_flat))

  tree, = treedef_children(in_args_tree)

  def _shape_checked(fun, name, has_aux):
    def f(x):
      y = fun(x)
      _check_shapes(name, "b", y, b_flat)
      return y

    def f_aux(x):
      y, aux = fun(x)
      _check_shapes(name, "b", y, b_flat)
      return y, aux

    return f_aux if has_aux else f

  # no auxiliary data assumed for matvec
  matvec_jaxpr, matvec_consts, out_tree = _initial_style_jaxpr(
      _shape_checked(matvec, "matvec", False), in_args_tree, b_avals,
      'custom_linear_solve')
  _check_tree("matvec", "b", out_tree, tree, False)

  solve_jaxpr, solve_consts, out_tree = _initial_style_jaxpr(
      _shape_checked(partial(solve, matvec), "solve", has_aux), in_args_tree, b_avals,
      'custom_linear_solve')
  _check_tree("solve", "b", out_tree, tree, has_aux)

  if transpose_solve is None:
    vecmat_jaxpr = tr_solve_jaxpr = None
    vecmat_consts = tr_solve_consts = []
  else:
    if symmetric:
      vecmat = matvec
      vecmat_jaxpr = matvec_jaxpr
      vecmat_consts = matvec_consts
    else:
      vecmat = _transpose_one_output(matvec, b)
      vecmat_jaxpr, vecmat_consts, out_tree = _initial_style_jaxpr(
          vecmat, in_args_tree, b_avals, 'custom_linear_solve')
      assert out_tree == tree

    tr_solve_jaxpr, tr_solve_consts, out_tree = _initial_style_jaxpr(
        _shape_checked(partial(transpose_solve, vecmat), "transpose_solve", has_aux),
        in_args_tree, b_avals, 'custom_linear_solve')
    _check_tree("transpose_solve", "b", out_tree, tree, has_aux)

  all_consts = [matvec_consts, vecmat_consts, solve_consts, tr_solve_consts]
  const_lengths = _LinearSolveTuple(*_map(len, all_consts))
  jaxprs = _LinearSolveTuple(
      matvec_jaxpr, vecmat_jaxpr, solve_jaxpr, tr_solve_jaxpr)

  out_flat = linear_solve_p.bind(
      *(_flatten(all_consts) + b_flat),
      const_lengths=const_lengths, jaxprs=jaxprs)

  return tree_unflatten(out_tree, out_flat)
