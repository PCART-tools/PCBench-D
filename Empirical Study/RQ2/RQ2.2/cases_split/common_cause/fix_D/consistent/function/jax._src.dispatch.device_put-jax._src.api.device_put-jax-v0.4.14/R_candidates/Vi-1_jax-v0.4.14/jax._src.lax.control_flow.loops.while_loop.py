@api_boundary
def while_loop(cond_fun: Callable[[T], BooleanNumeric],
               body_fun: Callable[[T], T],
               init_val: T) -> T:
  """Call ``body_fun`` repeatedly in a loop while ``cond_fun`` is True.

  The `Haskell-like type signature`_ in brief is

  .. code-block:: haskell

    while_loop :: (a -> Bool) -> (a -> a) -> a -> a

  The semantics of ``while_loop`` are given by this Python implementation::

    def while_loop(cond_fun, body_fun, init_val):
      val = init_val
      while cond_fun(val):
        val = body_fun(val)
      return val

  Unlike that Python version, ``while_loop`` is a JAX primitive and is lowered
  to a single WhileOp. That makes it useful for reducing compilation times
  for jit-compiled functions, since native Python loop constructs in an ``@jit``
  function are unrolled, leading to large XLA computations.

  Also unlike the Python analogue, the loop-carried value ``val`` must hold a
  fixed shape and dtype across all iterations (and not just be consistent up to
  NumPy rank/shape broadcasting and dtype promotion rules, for example). In
  other words, the type ``a`` in the type signature above represents an array
  with a fixed shape and dtype (or a nested tuple/list/dict container data
  structure with a fixed structure and arrays with fixed shape and dtype at the
  leaves).

  Another difference from using Python-native loop constructs is that
  ``while_loop`` is not reverse-mode differentiable because XLA computations
  require static bounds on memory requirements.

  .. note::
    :py:func:`while_loop` compiles ``cond_fun`` and ``body_fun``, so while it
    can be combined with :py:func:`jit`, it's usually unnecessary.

  Args:
    cond_fun: function of type ``a -> Bool``.
    body_fun: function of type ``a -> a``.
    init_val: value of type ``a``, a type that can be a scalar, array, or any
      pytree (nested Python tuple/list/dict) thereof, representing the initial
      loop carry value.

  Returns:
    The output from the final iteration of body_fun, of type ``a``.

  .. _Haskell-like type signature: https://wiki.haskell.org/Type_signature
  """
  if not (callable(body_fun) and callable(cond_fun)):
    raise TypeError("lax.while_loop: body_fun and cond_fun arguments should be callable.")
  if config.jax_disable_jit:
    try:
      val = init_val
      while cond_fun(val):
        val = body_fun(val)
      return val
    except core.ConcretizationTypeError:
      # Can't run this while_loop in Python (e.g. because there's a vmap
      # transformation on it), so we fall back to the primitive version.
      pass

  def _create_jaxpr(init_val):
    init_vals, in_tree = tree_flatten((init_val,))
    init_avals = tuple(_map(_abstractify, init_vals))
    cond_jaxpr, cond_consts, cond_tree = _initial_style_jaxpr(
        cond_fun, in_tree, init_avals, "while_cond")
    body_jaxpr, body_consts, body_tree = _initial_style_jaxpr(
        body_fun, in_tree, init_avals, "while_loop")
    if not treedef_is_leaf(cond_tree) or len(cond_jaxpr.out_avals) != 1:
      msg = "cond_fun must return a boolean scalar, but got pytree {}."
      raise TypeError(msg.format(cond_tree))
    pred_aval = cond_jaxpr.out_avals[0]
    if (not isinstance(pred_aval, ShapedArray)
        or pred_aval.strip_weak_type().strip_named_shape() != ShapedArray((), np.bool_)):
      msg = "cond_fun must return a boolean scalar, but got output type(s) {}."
      raise TypeError(msg.format(cond_jaxpr.out_avals))
    return init_vals, init_avals, body_jaxpr, in_tree, cond_jaxpr, cond_consts, body_consts, body_tree

  # The body input and output avals must match exactly. However, we want to account for
  # the case when init contains weakly-typed values (e.g. Python scalars), with avals that
  # may not match the output despite being compatible by virtue of their weak type.
  # To do this, we compute the jaxpr in two passes: first with the raw inputs, and if
  # necessary, a second time with modified init values.
  init_vals, init_avals, body_jaxpr, in_tree, *rest = _create_jaxpr(init_val)
  new_init_vals, changed = _promote_weak_typed_inputs(init_vals, init_avals, body_jaxpr.out_avals)
  if changed:
    new_init_val, = tree_unflatten(in_tree, new_init_vals)
    init_vals, init_avals, body_jaxpr, in_tree, *rest = _create_jaxpr(new_init_val)
  cond_jaxpr, cond_consts, body_consts, body_tree = rest

  in_tree_children = in_tree.children()
  assert len(in_tree_children) == 1
  _check_tree_and_avals("body_fun output and input",
                        body_tree, body_jaxpr.out_avals,
                        in_tree_children[0], init_avals)
  effects = core.join_effects(cond_jaxpr.effects, body_jaxpr.effects)
  disallowed_effects = allowed_effects.filter_not_in(effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `while`: {disallowed_effects}')
  outs = while_p.bind(*cond_consts, *body_consts, *init_vals,
                      cond_nconsts=len(cond_consts), cond_jaxpr=cond_jaxpr,
                      body_nconsts=len(body_consts), body_jaxpr=body_jaxpr)
  return tree_unflatten(body_tree, outs)
