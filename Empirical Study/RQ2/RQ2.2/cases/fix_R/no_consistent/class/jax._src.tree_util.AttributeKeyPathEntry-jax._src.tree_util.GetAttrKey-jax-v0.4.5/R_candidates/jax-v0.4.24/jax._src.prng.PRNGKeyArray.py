class PRNGKeyArray(jax.Array):
  """An array of PRNG keys backed by an RNG implementation.

  This class lifts the definition of a PRNG, provided in the form of a
  ``PRNGImpl``, into an array-like pytree class. Instances of this
  class behave like an array whose base elements are keys, hiding the
  fact that keys are typically arrays (of ``uint32`` dtype) themselves.

  PRNGKeyArrays are also restricted relative to JAX arrays in that
  they do not expose arithmetic operations. They instead expose
  wrapper methods around the PRNG implementation functions (``split``,
  ``random_bits``, ``fold_in``).
  """
  # TODO(jakevdp): potentially add tolist(), tobytes(),
  #    device_buffer, device_buffers, __cuda_interface__()

  _impl: PRNGImpl
  _base_array: typing.Array

  def __init__(self, impl, key_data: Any):
    assert not isinstance(key_data, core.Tracer)
    _check_prng_key_data(impl, key_data)
    self._impl = impl
    self._base_array = key_data

  def block_until_ready(self):
    _ = self._base_array.block_until_ready()
    return self

  def copy_to_host_async(self):
    _ = self._base_array.copy_to_host_async()

  @property
  def aval(self):
    return keys_shaped_array(self._impl, self.shape)

  @property
  def shape(self):
    return base_arr_shape_to_keys_shape(self._impl, self._base_array.shape)

  @property
  def size(self):
    return math.prod(self.shape)

  @property
  def ndim(self):
    return len(self.shape)

  @property
  def dtype(self):
    return KeyTy(self._impl)

  @property
  def itemsize(self):
    return self.dtype.itemsize

  _device = property(op.attrgetter('_base_array._device'))
  _committed = property(op.attrgetter('_base_array._committed'))
  device = property(op.attrgetter('_base_array.device'))  # type: ignore[assignment]
  devices = property(op.attrgetter('_base_array.devices'))  # type: ignore[assignment]
  is_fully_addressable = property(op.attrgetter('_base_array.is_fully_addressable'))  # type: ignore[assignment]
  is_fully_replicated = property(op.attrgetter('_base_array.is_fully_replicated'))  # type: ignore[assignment]
  delete = property(op.attrgetter('_base_array.delete'))  # type: ignore[assignment]
  is_deleted = property(op.attrgetter('_base_array.is_deleted'))  # type: ignore[assignment]
  on_device_size_in_bytes = property(op.attrgetter('_base_array.on_device_size_in_bytes'))  # type: ignore[assignment]
  unsafe_buffer_pointer = property(op.attrgetter('_base_array.unsafe_buffer_pointer'))  # type: ignore[assignment]

  def addressable_data(self, index: int) -> PRNGKeyArray:
    return PRNGKeyArray(self._impl, self._base_array.addressable_data(index))

  @property
  def addressable_shards(self) -> list[Shard]:
    return [
        type(s)(
            device=s._device,
            sharding=s._sharding,
            global_shape=s._global_shape,
            data=PRNGKeyArray(self._impl, s._data),
        )
        for s in self._base_array.addressable_shards
    ]

  @property
  def global_shards(self) -> list[Shard]:
    return [
        type(s)(
            device=s._device,
            sharding=s._sharding,
            global_shape=s._global_shape,
            data=PRNGKeyArray(self._impl, s._data),
        )
        for s in self._base_array.global_shards
    ]

  @property
  def sharding(self):
    phys_sharding = self._base_array.sharding
    return KeyTyRules.logical_op_sharding(self.aval, phys_sharding)

  def _is_scalar(self):
    base_ndim = len(self._impl.key_shape)
    return self._base_array.ndim == base_ndim

  def __len__(self):
    if self._is_scalar():
      raise TypeError('len() of unsized object')
    return len(self._base_array)

  def __iter__(self) -> Iterator[PRNGKeyArray]:
    if self._is_scalar():
      raise TypeError('iteration over a 0-d key array')
    # TODO(frostig): we may want to avoid iteration by slicing because
    # a very common use of iteration is `k1, k2 = split(key)`, and
    # slicing/indexing may be trickier to track for linearity checking
    # purposes. Maybe we can:
    # * introduce an unpack primitive+traceable (also allow direct use)
    # * unpack upfront into shape[0] many keyarray slices
    # * return iter over these unpacked slices
    # Whatever we do, we'll want to do it by overriding
    # ShapedArray._iter when the element type is KeyTy...
    return (PRNGKeyArray(self._impl, k) for k in iter(self._base_array))

  def __repr__(self):
    return (f'Array({self.shape}, dtype={self.dtype.name}) overlaying:\n'
            f'{self._base_array}')

  def pprint(self):
    pp_keys = pp.text('shape = ') + pp.text(str(self.shape))
    pp_impl = pp.text('impl = ') + self._impl.pprint()
    return str(pp.group(
      pp.text('PRNGKeyArray:') +
      pp.nest(2, pp.brk() + pp_keys + pp.brk() + pp_impl)))

  def copy(self):
    return self.__class__(self._impl, self._base_array.copy())

  __hash__ = None  # type: ignore[assignment]
  __array_priority__ = 100

  # Overwritten immediately below
  @property
  def at(self)                  -> _IndexUpdateHelper: assert False  # type: ignore[override]
  @property
  def T(self)                   -> PRNGKeyArray: assert False
  def __getitem__(self, _)      -> PRNGKeyArray: assert False
  def flatten(self, *_, **__)   -> PRNGKeyArray: assert False
  def ravel(self, *_, **__)     -> PRNGKeyArray: assert False
  def reshape(self, *_, **__)   -> PRNGKeyArray: assert False
  def squeeze(self, *_, **__)   -> PRNGKeyArray: assert False
  def swapaxes(self, *_, **__)  -> PRNGKeyArray: assert False
  def take(self, *_, **__)      -> PRNGKeyArray: assert False
  def transpose(self, *_, **__) -> PRNGKeyArray: assert False
