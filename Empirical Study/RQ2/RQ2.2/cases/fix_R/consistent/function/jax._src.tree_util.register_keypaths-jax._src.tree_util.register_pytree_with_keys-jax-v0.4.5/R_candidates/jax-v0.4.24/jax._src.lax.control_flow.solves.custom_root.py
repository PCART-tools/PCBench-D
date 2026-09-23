@api_boundary
def custom_root(f, initial_guess, solve, tangent_solve, has_aux=False):
  """Differentiably solve for a roots of a function.

  This is a low-level routine, mostly intended for internal use in JAX.
  Gradients of custom_root() are defined with respect to closed-over variables
  from the provided function ``f`` via the implicit function theorem:
  https://en.wikipedia.org/wiki/Implicit_function_theorem

  Args:
    f: function for which to find a root. Should accept a single argument,
      return a tree of arrays with the same structure as its input.
    initial_guess: initial guess for a zero of f.
    solve: function to solve for the roots of f. Should take two positional
      arguments, f and initial_guess, and return a solution with the same
      structure as initial_guess such that func(solution) = 0. In other words,
      the following is assumed to be true (but not checked)::

        solution = solve(f, initial_guess)
        error = f(solution)
        assert all(error == 0)

    tangent_solve: function to solve the tangent system. Should take two
      positional arguments, a linear function ``g`` (the function ``f``
      linearized at its root) and a tree of array(s) ``y`` with the same
      structure as initial_guess, and return a solution ``x`` such that
      ``g(x)=y``:

      - For scalar ``y``, use ``lambda g, y: y / g(1.0)``.
      - For vector ``y``, you could use a linear solve with the Jacobian, if
        dimensionality of ``y`` is not too large:
        ``lambda g, y: np.linalg.solve(jacobian(g)(y), y)``.
    has_aux: bool indicating whether the ``solve`` function returns
      auxiliary data like solver diagnostics as a second argument.

  Returns:
    The result of calling solve(f, initial_guess) with gradients defined via
    implicit differentiation assuming ``f(solve(f, initial_guess)) == 0``.
  """
  guess_flat, in_args_tree = tree_flatten((initial_guess,))
  guess_avals = tuple(_map(_abstractify, guess_flat))
  f_jaxpr, f_consts, out_tree = _initial_style_jaxpr(
      f, in_args_tree, guess_avals)

  in_tree, = treedef_children(in_args_tree)
  _check_tree("f", "initial_guess", out_tree, in_tree, False)

  solve_jaxpr, solve_consts, solution_tree = _initial_style_jaxpr(
      partial(solve, f), in_args_tree, guess_avals)
  _check_tree("solve", "initial_guess", solution_tree, in_tree, has_aux)

  def linearize_and_solve(x, b):
    unchecked_zeros, f_jvp = jax.linearize(f, x)
    return tangent_solve(f_jvp, b)

  l_and_s_jaxpr, l_and_s_consts, out_tree = _initial_style_jaxpr(
      linearize_and_solve, treedef_tuple((in_tree,) * 2), guess_avals * 2)
  _check_tree("tangent_solve", "x", out_tree, in_tree, False)

  all_consts = [f_consts, solve_consts, l_and_s_consts]
  const_lengths = _RootTuple(*_map(len, all_consts))
  jaxprs = _RootTuple(f_jaxpr, solve_jaxpr, l_and_s_jaxpr)

  solution_flat = _custom_root(
      const_lengths, jaxprs, *(_flatten(all_consts) + guess_flat))
  return tree_unflatten(solution_tree, solution_flat)
