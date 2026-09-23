@api_boundary
def scan(f: Callable[[Carry, X], tuple[Carry, Y]],
         init: Carry,
         xs: X,
         length: Optional[int] = None,
         reverse: bool = False,
         unroll: int = 1) -> tuple[Carry, Y]:
  """Scan a function over leading array axes while carrying along state.

  The `Haskell-like type signature`_ in brief is

  .. code-block:: haskell

    scan :: (c -> a -> (c, b)) -> c -> [a] -> (c, [b])

  where for any array type specifier ``t``, ``[t]`` represents the type with an additional
  leading axis, and if ``t`` is a pytree (container) type with array leaves then ``[t]``
  represents the type with the same pytree structure and corresponding leaves
  each with an additional leading axis.

  When the type of ``xs`` (denoted `a` above) is an array type or None, and the type
  of ``ys`` (denoted `b` above) is an array type, the semantics of :func:`~scan` are
  given roughly by this Python implementation::

    def scan(f, init, xs, length=None):
      if xs is None:
        xs = [None] * length
      carry = init
      ys = []
      for x in xs:
        carry, y = f(carry, x)
        ys.append(y)
      return carry, np.stack(ys)

  Unlike that Python version, both ``xs`` and ``ys`` may be arbitrary pytree
  values, and so multiple arrays can be scanned over at once and produce multiple
  output arrays. ``None`` is actually a special case of this, as it represents an
  empty pytree.

  Also unlike that Python version, :func:`~scan` is a JAX primitive and is
  lowered to a single WhileOp. That makes it useful for reducing
  compilation times for JIT-compiled functions, since native Python
  loop constructs in an :func:`~jax.jit` function are unrolled, leading to large
  XLA computations.

  Finally, the loop-carried value ``carry`` must hold a fixed shape and dtype
  across all iterations (and not just be consistent up to NumPy rank/shape
  broadcasting and dtype promotion rules, for example). In other words, the type
  ``c`` in the type signature above represents an array with a fixed shape and
  dtype (or a nested tuple/list/dict container data structure with a fixed
  structure and arrays with fixed shape and dtype at the leaves).

  .. note::
    :py:func:`scan` compiles ``f``, so while it can be combined with
    :py:func:`jit`, it's usually unnecessary.

  Args:
    f: a Python function to be scanned of type ``c -> a -> (c, b)``, meaning
      that ``f`` accepts two arguments where the first is a value of the loop
      carry and the second is a slice of ``xs`` along its leading axis, and that
      ``f`` returns a pair where the first element represents a new value for
      the loop carry and the second represents a slice of the output.
    init: an initial loop carry value of type ``c``, which can be a scalar,
      array, or any pytree (nested Python tuple/list/dict) thereof, representing
      the initial loop carry value. This value must have the same structure as
      the first element of the pair returned by ``f``.
    xs: the value of type ``[a]`` over which to scan along the leading axis,
      where ``[a]`` can be an array or any pytree (nested Python
      tuple/list/dict) thereof with consistent leading axis sizes.
    length: optional integer specifying the number of loop iterations, which
      must agree with the sizes of leading axes of the arrays in ``xs`` (but can
      be used to perform scans where no input ``xs`` are needed).
    reverse: optional boolean specifying whether to run the scan iteration
      forward (the default) or in reverse, equivalent to reversing the leading
      axes of the arrays in both ``xs`` and in ``ys``.
    unroll: optional positive int specifying, in the underlying operation of the
      scan primitive, how many scan iterations to unroll within a single
      iteration of a loop.

  Returns:
    A pair of type ``(c, [b])`` where the first element represents the final
    loop carry value and the second element represents the stacked outputs of
    the second output of ``f`` when scanned over the leading axis of the inputs.

  .. _Haskell-like type signature: https://wiki.haskell.org/Type_signature
  """
  if not callable(f):
    raise TypeError("lax.scan: f argument should be a callable.")
  xs_flat, xs_tree = tree_flatten(xs)

  try:
    lengths = [x.shape[0] for x in xs_flat]
  except AttributeError as err:
    msg = "scan got value with no leading axis to scan over: {}."
    raise ValueError(
      msg.format(', '.join(str(x) for x in xs_flat
                           if not hasattr(x, 'shape')))) from err

  if length is not None:
    length = int(length)
    if not all(length == l for l in lengths):
      msg = ("scan got `length` argument of {} which disagrees with "
             "leading axis sizes {}.")
      raise ValueError(msg.format(length, [x.shape[0] for x in xs_flat]))
  else:
    unique_lengths = set(lengths)
    if len(unique_lengths) > 1:
      msg = "scan got values with different leading axis sizes: {}."
      raise ValueError(msg.format(', '.join(str(x.shape[0]) for x in xs_flat)))
    elif len(unique_lengths) == 0:
      msg = "scan got no values to scan over and `length` not provided."
      raise ValueError(msg)
    else:
      length, = unique_lengths

  if config.jax_disable_jit:
    if length == 0:
      raise ValueError("zero-length scan is not supported in disable_jit() mode because the output type is unknown.")
    carry = init
    ys = []
    maybe_reversed = reversed if reverse else lambda x: x
    for i in maybe_reversed(range(length)):
      xs_slice = [_index_array(i, core.get_aval(x), x) for x in xs_flat]
      carry, y = f(carry, tree_unflatten(xs_tree, xs_slice))
      ys.append(y)
    stack = lambda *ys: jax.numpy.stack(ys)
    stacked_y = tree_map(stack, *maybe_reversed(ys))
    return carry, stacked_y

  xs_avals = [core.raise_to_shaped(core.get_aval(x)) for x in xs_flat]
  x_avals = [core.mapped_aval(length, 0, aval) for aval in xs_avals]

  def _create_jaxpr(init):
    init_flat, init_tree = tree_flatten(init)
    in_flat, in_tree = tree_flatten((init, xs))

    carry_avals = tuple(_map(_abstractify, init_flat))
    jaxpr, consts, out_tree = _initial_style_jaxpr(
        f, in_tree, (*carry_avals, *x_avals), "scan")
    out_tree_children = out_tree.children()
    if len(out_tree_children) != 2:
      msg = "scan body output must be a pair, got {}."
      raise TypeError(msg.format(tree_unflatten(out_tree, jaxpr.out_avals)))
    carry_avals_out = jaxpr.out_avals[:out_tree_children[0].num_leaves]
    return init_flat, carry_avals, carry_avals_out, init_tree, in_flat, jaxpr, consts, out_tree, out_tree_children

  # The carry input and output avals must match exactly. However, we want to account for
  # the case when init contains weakly-typed values (e.g. Python scalars), with avals that
  # may not match the output despite being compatible by virtue of their weak type.
  # To do this, we compute the jaxpr in two passes: first with the raw inputs, and if
  # necessary, a second time with modified init values.
  init_flat, carry_avals, carry_avals_out, init_tree, *rest = _create_jaxpr(init)
  new_init_flat, changed = _promote_weak_typed_inputs(init_flat, carry_avals, carry_avals_out)
  if changed:
    init = tree_unflatten(init_tree, new_init_flat)
    init_flat, carry_avals, carry_avals_out, init_tree, *rest = _create_jaxpr(init)
  in_flat, jaxpr, consts, out_tree, out_tree_children = rest

  _check_scan_carry_type(f, init, out_tree_children[0], carry_avals_out)
  disallowed_effects = allowed_effects.filter_not_in(jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `scan`: {disallowed_effects}')

  out = scan_p.bind(*consts, *in_flat,
                    reverse=reverse, length=length, jaxpr=jaxpr,
                    num_consts=len(consts), num_carry=len(init_flat),
                    linear=(False,) * (len(consts) + len(in_flat)),
                    unroll=unroll)
  return tree_unflatten(out_tree, out)
