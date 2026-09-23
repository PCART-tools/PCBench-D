@api_boundary
def associative_scan(fn: Callable, elems, reverse: bool = False, axis: int = 0):
  """Performs a scan with an associative binary operation, in parallel.

  For an introduction to associative scans, see [BLE1990]_.

  Args:
    fn: A Python callable implementing an associative binary operation with
      signature ``r = fn(a, b)``. Function `fn` must be associative, i.e., it
      must satisfy the equation
      ``fn(a, fn(b, c)) == fn(fn(a, b), c)``.

      The inputs and result are (possibly nested Python tree structures of)
      array(s) matching ``elems``. Each array has a dimension in place
      of the ``axis`` dimension. `fn` should be applied elementwise over
      the ``axis`` dimension (for example, by using :func:`jax.vmap` over the
      elementwise function.)

      The result ``r`` has the same shape (and structure) as the two inputs
      ``a`` and ``b``.
    elems: A (possibly nested Python tree structure of) array(s), each with
      an ``axis`` dimension of size ``num_elems``.
    reverse: A boolean stating if the scan should be reversed with respect to
      the ``axis`` dimension.
    axis: an integer identifying the axis over which the scan should occur.

  Returns:
    A (possibly nested Python tree structure of) array(s) of the same shape
    and structure as ``elems``, in which the ``k``'th element of ``axis`` is the
    result of recursively applying ``fn`` to combine the first ``k`` elements
    of ``elems`` along ``axis``. For example, given ``elems = [a, b, c, ...]``,
    the result would be ``[a, fn(a, b), fn(fn(a, b), c), ...]``.

  Example 1: partial sums of an array of numbers:

  >>> lax.associative_scan(jnp.add, jnp.arange(0, 4))
  DeviceArray([0, 1, 3, 6], dtype=int32)

  Example 2: partial products of an array of matrices

  >>> mats = jax.random.uniform(jax.random.PRNGKey(0), (4, 2, 2))
  >>> partial_prods = lax.associative_scan(jnp.matmul, mats)
  >>> partial_prods.shape
  (4, 2, 2)

  Example 3: reversed partial sums of an array of numbers

  >>> lax.associative_scan(jnp.add, jnp.arange(0, 4), reverse=True)
  DeviceArray([6, 6, 5, 3], dtype=int32)

  .. [BLE1990] Blelloch, Guy E. 1990. "Prefix Sums and Their Applications.",
    Technical Report CMU-CS-90-190, School of Computer Science, Carnegie Mellon
    University.
  """
  if not callable(fn):
    raise TypeError("lax.associative_scan: fn argument should be callable.")
  elems_flat, tree = tree_flatten(elems)

  if reverse:
    elems_flat = [lax.rev(elem, [axis]) for elem in elems_flat]

  def combine(a_flat, b_flat):
    # Lower `fn` to operate on flattened sequences of elems.
    a = tree_unflatten(tree, a_flat)
    b = tree_unflatten(tree, b_flat)
    c = fn(a, b)
    c_flat, _ = tree_flatten(c)
    return c_flat

  # Check that all inputs have a consistent leading dimension `num_elems`.
  axis = util.canonicalize_axis(axis, elems_flat[0].ndim)
  num_elems = int(elems_flat[0].shape[axis])
  if not all(int(elem.shape[axis]) == num_elems for elem in elems_flat[1:]):
    raise ValueError('Array inputs to associative_scan must have the same '
                     'first dimension. (saw: {})'
                     .format([elem.shape for elem in elems_flat]))


  # Summary of algorithm:
  #
  # Consider elements of `_scan(elems)` at odd indices. That's the same as first
  # summing successive pairs of elements of `elems` and performing a scan on
  # that half sized tensor. We perform the latter scan by recursion.
  #
  # Now consider the even elements of `_scan(elems)`. These can be computed
  # from the odd elements of `_scan(elems)` by adding each odd element of
  # `_scan(elems)` to the matching even element in the original `elems`.
  #
  # We return the odd and even elements interleaved.
  #
  # For the base case of the recursion we return the first element
  # of `elems` followed by the sum of the first two elements computed as
  # a (small two-down-to-one) reduction step.
  def _scan(elems):
    """Perform scan on `elems`."""

    num_elems = elems[0].shape[axis]

    if num_elems < 2:
      return elems

    # Combine adjacent pairs of elements.
    reduced_elems = combine(
      [slicing.slice_in_dim(elem, 0, -1, stride=2, axis=axis) for elem in elems],
      [slicing.slice_in_dim(elem, 1, None, stride=2, axis=axis)
       for elem in elems])

    # Recursively compute scan for partially reduced tensors.
    odd_elems = _scan(reduced_elems)

    if num_elems % 2 == 0:
      even_elems = combine(
        [slicing.slice_in_dim(e, 0, -1, axis=axis) for e in odd_elems],
        [slicing.slice_in_dim(e, 2, None, stride=2, axis=axis) for e in elems])
    else:
      even_elems = combine(
        odd_elems,
        [slicing.slice_in_dim(e, 2, None, stride=2, axis=axis) for e in elems])

    # The first element of a scan is the same as the first element
    # of the original `elems`.
    even_elems = [
      lax.concatenate([slicing.slice_in_dim(elem, 0, 1, axis=axis), result],
                      dimension=axis)
      for (elem, result) in zip(elems, even_elems)]
    return list(_map(partial(_interleave, axis=axis), even_elems, odd_elems))

  scans = _scan(elems_flat)

  if reverse:
    scans = [lax.rev(scanned, [axis]) for scanned in scans]

  return tree_unflatten(tree, scans)
