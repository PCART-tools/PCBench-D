@tree_util.register_pytree_node_class
class PRNGKeyArray:
  """An array whose elements are PRNG keys.

  This class lifts the definition of a PRNG, provided in the form of a
  ``PRNGImpl``, into an array-like pytree class. Instances of this
  class behave like an array whose base elements are keys, hiding the
  fact that keys are typically arrays (of ``uint32`` dtype) themselves.

  PRNGKeyArrays are also restricted relative to JAX arrays in that
  they do not expose arithmetic operations. They instead expose
  wrapper methods around the PRNG implementation functions (``split``,
  ``random_bits``, ``fold_in``).
  """

  impl: PRNGImpl
  _keys: jnp.ndarray

  def __init__(self, impl, key_data: jnp.ndarray):
    # key_data might be a placeholder python `object` or `bool`
    # instead of a jnp.ndarray due to tree_unflatten
    if type(key_data) not in [object, bool]:
      _check_prng_key_data(impl, key_data)
    self.impl = impl
    self._keys = key_data

  def tree_flatten(self):
    return (self._keys,), self.impl

  def unsafe_raw_array(self):
    """Access the raw numerical array that carries underlying key data.

    Returns:
      A uint32 JAX array whose leading dimensions are ``self.shape``.
    """
    return self._keys

  @classmethod
  def tree_unflatten(cls, impl, keys):
    keys, = keys
    return cls(impl, keys)

  @property
  def dtype(self):
    # TODO(frostig): remove after deprecation window
    if config.jax_enable_custom_prng:
      raise AttributeError("'PRNGKeyArray' has no attribute 'dtype'")
    else:
      warnings.warn(
          'deprecated `dtype` attribute of PRNG key arrays', FutureWarning)
      return np.uint32

  @property
  def shape(self):
    # TODO(frostig): simplify once we always enable_custom_prng
    if config.jax_enable_custom_prng:
      return self._shape
    else:
      warnings.warn(
          'deprecated `shape` attribute of PRNG key arrays. In a future version '
          'of JAX this attribute will be removed or its value may change.',
          FutureWarning)
      return self._keys.shape

  @property
  def _shape(self):
    base_ndim = len(self.impl.key_shape)
    return self._keys.shape[:-base_ndim]

  @property
  def ndim(self):
    return len(self.shape)

  def _is_scalar(self):
    base_ndim = len(self.impl.key_shape)
    return self._keys.ndim == base_ndim

  def __len__(self):
    if self._is_scalar():
      raise TypeError('len() of unsized object')
    return len(self._keys)

  def __iter__(self) -> Iterator['PRNGKeyArray']:
    if self._is_scalar():
      raise TypeError('iteration over a 0-d single PRNG key')
    return (PRNGKeyArray(self.impl, k) for k in iter(self._keys))

  def __getitem__(self, idx) -> 'PRNGKeyArray':
    base_ndim = len(self.impl.key_shape)
    ndim = self._keys.ndim - base_ndim
    indexable_shape = self.impl.key_shape[:ndim]
    idx = _eliminate_deprecated_list_indexing(idx)
    idx = _expand_bool_indices(idx, indexable_shape)
    idx = _canonicalize_tuple_index(ndim, idx, array_name='PRNGKeyArray')
    return PRNGKeyArray(self.impl, self._keys[idx])

  def _fold_in(self, data: int) -> 'PRNGKeyArray':
    return PRNGKeyArray(self.impl, self.impl.fold_in(self._keys, data))

  def _random_bits(self, bit_width, shape) -> jnp.ndarray:
    return self.impl.random_bits(self._keys, bit_width, shape)

  def _split(self, num: int) -> 'PRNGKeyArray':
    return PRNGKeyArray(self.impl, self.impl.split(self._keys, num))

  def reshape(self, newshape, order=None):
    reshaped_keys = jnp.reshape(self._keys, (*newshape, -1), order=order)
    return PRNGKeyArray(self.impl, reshaped_keys)

  def concatenate(self, key_arrs, axis):
    axis = canonicalize_axis(axis, self.ndim)
    arrs = [self._keys, *[k._keys for k in key_arrs]]
    return PRNGKeyArray(self.impl, jnp.concatenate(arrs, axis))

  def broadcast_to(self, shape):
    if jnp.ndim(shape) == 0:
      shape = (shape,)
    new_shape = (*shape, *self.impl.key_shape)
    return PRNGKeyArray(self.impl, jnp.broadcast_to(self._keys, new_shape))

  def expand_dims(self, dimensions: Sequence[int]):
    # follows lax.expand_dims, not jnp.expand_dims, so dimensions is a sequence
    ndim_out = self.ndim + len(set(dimensions))
    dimensions = [canonicalize_axis(d, ndim_out) for d in dimensions]
    return PRNGKeyArray(self.impl, lax.expand_dims(self._keys, dimensions))

  def __repr__(self):
    arr_shape = self._shape
    pp_keys = pp.text('shape = ') + pp.text(str(arr_shape))
    pp_impl = pp.text('impl = ') + self.impl.pprint()
    return str(pp.group(
      pp.text('PRNGKeyArray:') +
      pp.nest(2, pp.brk() + pp_keys + pp.brk() + pp_impl)))
