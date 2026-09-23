def choice(key: KeyArray,
           a: Union[int, ArrayLike],
           shape: Shape = (),
           replace: bool = True,
           p: Optional[RealArray] = None,
           axis: int = 0) -> Array:
  """Generates a random sample from a given array.

  .. warning::
    If ``p`` has fewer non-zero elements than the requested number of samples,
    as specified in ``shape``, and ``replace=False``, the output of this
    function is ill-defined. Please make sure to use appropriate inputs.

  Args:
    key: a PRNG key used as the random key.
    a : array or int. If an ndarray, a random sample is generated from
      its elements. If an int, the random sample is generated as if a were
      arange(a).
    shape : tuple of ints, optional. Output shape.  If the given shape is,
      e.g., ``(m, n)``, then ``m * n`` samples are drawn.  Default is (),
      in which case a single value is returned.
    replace : boolean.  Whether the sample is with or without replacement.
      default is True.
    p : 1-D array-like, The probabilities associated with each entry in a.
      If not given the sample assumes a uniform distribution over all
      entries in a.
    axis: int, optional. The axis along which the selection is performed.
      The default, 0, selects by row.

  Returns:
    An array of shape `shape` containing samples from `a`.
  """
  key, _ = _check_prng_key(key)
  if not isinstance(shape, Sequence):
    raise TypeError("shape argument of jax.random.choice must be a sequence, "
                    f"got {shape}")
  _check_arraylike("choice", a)
  arr = jnp.asarray(a)
  if arr.ndim == 0:
    n_inputs = core.concrete_or_error(int, a, "The error occurred in jax.random.choice()")
  else:
    axis = canonicalize_axis(axis, arr.ndim)
    n_inputs = arr.shape[axis]
  n_draws = math.prod(shape)
  if n_draws == 0:
    return jnp.zeros(shape, dtype=arr.dtype)
  if n_inputs <= 0:
    raise ValueError("a must be greater than 0 unless no samples are taken")
  if not replace and n_draws > n_inputs:
    raise ValueError("Cannot take a larger sample than population when 'replace=False'")

  if p is None:
    if replace:
      ind = randint(key, shape, 0, n_inputs)
      result = ind if arr.ndim == 0 else jnp.take(arr, ind, axis)
    else:
      slices = (slice(None),) * axis + (slice(n_draws),)
      result = permutation(key, n_inputs if arr.ndim == 0 else arr, axis)[slices]
  else:
    _check_arraylike("choice", p)
    p_arr, = _promote_dtypes_inexact(p)
    if p_arr.shape != (n_inputs,):
      raise ValueError("p must be None or match the shape of a")
    if replace:
      p_cuml = jnp.cumsum(p_arr)
      r = p_cuml[-1] * (1 - uniform(key, shape, dtype=p_cuml.dtype))
      ind = jnp.searchsorted(p_cuml, r)
    else:
      # Gumbel top-k trick: https://timvieira.github.io/blog/post/2019/09/16/algorithms-for-sampling-without-replacement/
      g = -gumbel(key, (n_inputs,), dtype=p_arr.dtype) - jnp.log(p_arr)
      ind = jnp.argsort(g)[:n_draws]
    result = ind if arr.ndim == 0 else jnp.take(arr, ind, axis)

  return result.reshape(shape if arr.ndim == 0 else
                        np.insert(np.delete(arr.shape, axis), axis, shape))
