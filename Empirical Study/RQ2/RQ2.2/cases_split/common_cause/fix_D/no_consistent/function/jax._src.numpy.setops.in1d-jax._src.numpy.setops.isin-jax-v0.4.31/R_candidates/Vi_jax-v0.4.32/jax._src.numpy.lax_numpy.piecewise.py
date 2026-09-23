def piecewise(x: ArrayLike, condlist: Array | Sequence[ArrayLike],
              funclist: list[ArrayLike | Callable[..., Array]],
              *args, **kw) -> Array:
  """Evaluate a function defined piecewise across the domain.

  JAX implementation of :func:`numpy.piecewise`, in terms of :func:`jax.lax.switch`.

  Note:
    Unlike :func:`numpy.piecewise`, :func:`jax.numpy.piecewise` requires functions
    in ``funclist`` to be traceable by JAX, as it is implemented via
    :func:`jax.lax.switch`.

  Args:
    x: array of input values.
    condlist: boolean array or sequence of boolean arrays corresponding to the
      functions in ``funclist``. If a sequence of arrays, the length of each
      array must match the length of ``x``
    funclist: list of arrays or functions; must either be the same length as
      ``condlist``, or have length ``len(condlist) + 1``, in which case the
      last entry is the default applied when none of the conditions are True.
      Alternatively, entries of ``funclist`` may be numerical values, in which
      case they indicate a constant function.
    args, kwargs: additional arguments are passed to each function in
      ``funclist``.

  Returns:
    An array which is the result of evaluating the functions on ``x`` at
    the specified conditions.

  See also:
    - :func:`jax.lax.switch`: choose between *N* functions based on an index.
    - :func:`jax.lax.cond`: choose between two functions based on a boolean condition.
    - :func:`jax.numpy.where`: choose between two results based on a boolean mask.
    - :func:`jax.lax.select`: choose between two results based on a boolean mask.
    - :func:`jax.lax.select_n`: choose between *N* results based on a boolean mask.

  Examples:
    Here's an example of a function which is zero for negative values, and linear
    for positive values:

    >>> x = jnp.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])

    >>> condlist = [x < 0, x >= 0]
    >>> funclist = [lambda x: 0 * x, lambda x: x]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([0, 0, 0, 0, 0, 1, 2, 3, 4], dtype=int32)

    ``funclist`` can also contain a simple scalar value for constant functions:

    >>> condlist = [x < 0, x >= 0]
    >>> funclist = [0, lambda x: x]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([0, 0, 0, 0, 0, 1, 2, 3, 4], dtype=int32)

    You can specify a default value by appending an extra condition to ``funclist``:

    >>> condlist = [x < -1, x > 1]
    >>> funclist = [lambda x: 1 + x, lambda x: x - 1, 0]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([-3, -2,  -1,  0,  0,  0,  1,  2, 3], dtype=int32)

    ``condlist`` may also be a simple array of scalar conditions, in which case
    the associated function applies to the whole range

    >>> condlist = jnp.array([False, True, False])
    >>> funclist = [lambda x: x * 0, lambda x: x * 10, lambda x: x * 100]
    >>> jnp.piecewise(x, condlist, funclist)
    Array([-40, -30, -20, -10,   0,  10,  20,  30,  40], dtype=int32)
  """
  util.check_arraylike("piecewise", x)
  nc, nf = len(condlist), len(funclist)
  if nf == nc + 1:
    funclist = funclist[-1:] + funclist[:-1]
  elif nf == nc:
    funclist = [0] + list(funclist)
  else:
    raise ValueError(f"with {nc} condition(s), either {nc} or {nc+1} functions are expected; got {nf}")
  consts = {i: c for i, c in enumerate(funclist) if not callable(c)}
  funcs = {i: f for i, f in enumerate(funclist) if callable(f)}
  return _piecewise(asarray(x), asarray(condlist, dtype=bool_), consts,
                    frozenset(funcs.items()),  # dict is not hashable.
                    *args, **kw)
