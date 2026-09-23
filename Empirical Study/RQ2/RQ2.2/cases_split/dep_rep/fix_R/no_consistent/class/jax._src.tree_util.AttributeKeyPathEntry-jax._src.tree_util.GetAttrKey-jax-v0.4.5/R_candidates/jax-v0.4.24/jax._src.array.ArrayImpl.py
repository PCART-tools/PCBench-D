class ArrayImpl(basearray.Array):
  # TODO(yashkatariya): Add __slots__ here.

  aval: core.ShapedArray
  _sharding: Sharding
  _arrays: list[ArrayImpl]
  _committed: bool
  _skip_checks: bool
  _npy_value: np.ndarray | None

  @use_cpp_method()
  def __init__(self, aval: core.ShapedArray, sharding: Sharding,
               arrays: Sequence[ArrayImpl],
               committed: bool, _skip_checks: bool = False):
    # NOTE: the actual implementation of the constructor is moved to C++.

    self.aval = aval
    self._sharding = sharding
    self._arrays = [a._arrays[0] for a in arrays]
    self._committed = committed
    self._npy_value = None

    # Don't rearrange if skip_checks is enabled because this assumes that the
    # input buffers are already arranged properly. This usually happens when
    # Array's are created as output of a JAX transformation
    # (like pjit, xmap, etc).
    if not _skip_checks or config.enable_checks.value:
      self._check_and_rearrange()

  def _check_and_rearrange(self):
    for db in self._arrays:
      if db.dtype != self.dtype:
        raise ValueError(
            "Input buffers to `Array` must have matching dtypes. "
            f"Got {db.dtype}, expected {self.dtype} for buffer: {db}")

    device_id_to_buffer = {_get_device(db).id: db for db in self._arrays}

    addressable_dev = self.sharding.addressable_devices
    if len(self._arrays) != len(addressable_dev):
      raise ValueError(
          f"Expected {len(addressable_dev)} per-device arrays "
          "(this is how many devices are addressable by the sharding), but "
          f"got {len(self._arrays)}")

    array_device_ids = set(device_id_to_buffer.keys())
    addressable_device_ids = {d.id for d in addressable_dev}
    # Calculate a symmetric difference because the device ids between sharding
    # and _arrays should match.
    diff = array_device_ids ^ addressable_device_ids
    if diff:
      dev_in_sharding_not_in_arrays = addressable_device_ids - array_device_ids
      dev_in_arrays_not_in_sharding = array_device_ids - addressable_device_ids
      err_msg = (
          "Addressable devices and per-device arrays devices do not match.")
      if dev_in_sharding_not_in_arrays:
        err_msg += (f" Sharding contains devices {dev_in_sharding_not_in_arrays} "
                    "that are not present in per-device arrays.")
      if dev_in_arrays_not_in_sharding:
        err_msg += (f" Per-device arrays contain devices {dev_in_arrays_not_in_sharding} "
                    "that are not present in the sharding.")
      raise ValueError(err_msg)

    ss = self.sharding.shard_shape(self.shape)
    for db in self._arrays:
      if db.shape != ss:
        raise ValueError(
            f"Expected shard shape {ss} doesn't match the single device array "
            f"shape {db.shape}. Shape of Array is "
            f"{self.aval.str_short()} with sharding {self.sharding}")

    # Rearrange arrays based on the device assignment.
    if isinstance(self.sharding, XLACompatibleSharding):
      addressable_da = self.sharding._addressable_device_assignment
      self._arrays = [device_id_to_buffer[device.id] for device in addressable_da]

  @property
  def shape(self) -> Shape:
    return self.aval.shape

  @property
  def dtype(self):
    return self.aval.dtype

  @property
  def ndim(self):
    return len(self.shape)

  @property
  def size(self):
    return math.prod(self.shape)

  @property
  def sharding(self):
    return self._sharding

  @property
  def weak_type(self):
    return self.aval.weak_type

  def __str__(self):
    return str(self._value)

  def __len__(self):
    try:
      return self.shape[0]
    except IndexError as err:
      raise TypeError("len() of unsized object") from err  # same as numpy error

  def __bool__(self):
    core.check_bool_conversion(self)
    return bool(self._value)

  def __float__(self):
    core.check_scalar_conversion(self)
    return self._value.__float__()

  def __int__(self):
    core.check_scalar_conversion(self)
    return self._value.__int__()

  def __complex__(self):
    core.check_scalar_conversion(self)
    return self._value.__complex__()

  def __hex__(self):
    core.check_integer_conversion(self)
    return hex(self._value)  # type: ignore

  def __oct__(self):
    core.check_integer_conversion(self)
    return oct(self._value)  # type: ignore

  def __index__(self):
    core.check_integer_conversion(self)
    return op.index(self._value)

  def tobytes(self, order="C"):
    return self._value.tobytes(order)

  def tolist(self):
    return self._value.tolist()

  def __format__(self, format_spec):
    # Simulates behavior of https://github.com/numpy/numpy/pull/9883
    if self.ndim == 0:
      return format(self._value[()], format_spec)
    else:
      return format(self._value, format_spec)

  def __getitem__(self, idx):
    from jax._src.lax import lax
    from jax._src.numpy import lax_numpy
    self._check_if_deleted()

    if isinstance(idx, tuple):
      num_idx = sum(e is not None and e is not Ellipsis for e in idx)
      if num_idx > self.ndim:
        raise IndexError(
            f"Too many indices for array: array has ndim of {self.ndim}, but "
            f"was indexed with {num_idx} non-None/Ellipsis indices.")

    if isinstance(self.sharding, PmapSharding):
      if config.pmap_no_rank_reduction.value:
        cidx = idx if isinstance(idx, tuple) else (idx,)

        padded_cidx = tuple(
            slice(i, i + 1, None) if isinstance(i, int) else i for i in cidx
        ) + (slice(None),) * (len(self.shape) - len(cidx))
      else:
        if not isinstance(idx, tuple):
          padded_cidx = (idx,) + (slice(None),) * (len(self.shape) - 1)
        else:
          padded_cidx = idx + (slice(None),) * (len(self.shape) - len(idx))

      indices = tuple(self.sharding.devices_indices_map(self.shape).values())
      try:
        arr_idx = indices.index(padded_cidx)
      except ValueError:
        arr_idx = None
      if arr_idx is not None:
        a = self._arrays[arr_idx]
        out = ArrayImpl(
            a.aval, SingleDeviceSharding(_get_device(a)), [a], committed=False,
            _skip_checks=True)

        if config.pmap_no_rank_reduction.value:
          # If cidx was the index of a single shard, then it corresponds to one
          # shard of the chunked dimension.
          dims = tuple(i for i, x in enumerate(cidx) if isinstance(x, int))
          return lax.squeeze(out, dimensions=dims)
        else:
          return out

    return lax_numpy._rewriting_take(self, idx)

  def __iter__(self):
    if self.ndim == 0:
      raise TypeError("iteration over a 0-d array")  # same as numpy error
    else:
      assert self.is_fully_replicated or self.is_fully_addressable
      if dispatch.is_single_device_sharding(self.sharding) or self.is_fully_replicated:
        return (sl for chunk in self._chunk_iter(100) for sl in chunk._unstack())  # type: ignore
      elif isinstance(self.sharding, PmapSharding):
        return (self[i] for i in range(self.shape[0]))  # type: ignore
      else:
        # TODO(yashkatariya): Don't bounce to host and use `_chunk_iter` path
        # here after uneven partitioning support is added.
        return (api.device_put(self._value[i]) for i in range(self.shape[0]))

  @property
  def is_fully_replicated(self) -> bool:
    return self.sharding.is_fully_replicated

  def __repr__(self):
    prefix = 'Array('
    if self.aval is not None and self.aval.weak_type:
      dtype_str = f'dtype={self.dtype.name}, weak_type=True)'
    else:
      dtype_str = f'dtype={self.dtype.name})'

    if self.is_fully_addressable or self.is_fully_replicated:
      line_width = np.get_printoptions()["linewidth"]
      if self.size == 0:
        s = f"[], shape={self.shape}"
      else:
        s = np.array2string(self._value, prefix=prefix, suffix=',',
                            separator=', ', max_line_width=line_width)
      last_line_len = len(s) - s.rfind('\n') + 1
      sep = ' '
      if last_line_len + len(dtype_str) + 1 > line_width:
        sep = ' ' * len(prefix)
      return f"{prefix}{s},{sep}{dtype_str}"
    else:
      return f"{prefix}{self.shape}, {dtype_str}"

  @property
  def is_fully_addressable(self) -> bool:
    """Is this Array fully addressable?

    A jax.Array is fully addressable if the current process can address all of
    the devices named in the :class:`Sharding`. ``is_fully_addressable`` is
    equivalent to "is_local" in multi-process JAX.

    Note that fully replicated is not equal to fully addressable i.e.
    a jax.Array which is fully replicated can span across multiple hosts and is
    not fully addressable.
    """
    return self.sharding.is_fully_addressable

  def __array__(self, dtype=None, context=None):
    return np.asarray(self._value, dtype=dtype)

  def __dlpack__(self, *, stream: int | Any | None = None):
    if len(self._arrays) != 1:
      raise ValueError("__dlpack__ only supported for unsharded arrays.")
    from jax._src.dlpack import to_dlpack  # pylint: disable=g-import-not-at-top
    return to_dlpack(self, stream=stream)

  def __dlpack_device__(self) -> tuple[enum.Enum, int]:
    if len(self._arrays) != 1:
      raise ValueError("__dlpack__ only supported for unsharded arrays.")

    from jax._src.dlpack import DLDeviceType  # pylint: disable=g-import-not-at-top

    if self.platform() == "cpu":
      return DLDeviceType.kDLCPU, 0

    elif self.platform() == "gpu":
      platform_version = _get_device(self).client.platform_version
      if "cuda" in platform_version:
        dl_device_type = DLDeviceType.kDLCUDA
      elif "rocm" in platform_version:
        dl_device_type = DLDeviceType.kDLROCM
      else:
        raise ValueError("Unknown GPU platform for __dlpack__: "
                         f"{platform_version}")

      local_hardware_id = _get_device(self).local_hardware_id
      if local_hardware_id is None:
        raise ValueError("Couldn't get local_hardware_id for __dlpack__")

      return dl_device_type, local_hardware_id

    else:
      raise ValueError(
          "__dlpack__ device only supported for CPU and GPU, got platform: "
          f"{self.platform()}"
      )

  def __reduce__(self):
    fun, args, arr_state = self._value.__reduce__()  # type: ignore
    aval_state = {'weak_type': self.aval.weak_type,
                  'named_shape': self.aval.named_shape}
    return (_reconstruct_array, (fun, args, arr_state, aval_state))

  @use_cpp_method()
  def unsafe_buffer_pointer(self):
    if len(self._arrays) != 1:
      raise ValueError("unsafe_buffer_pointer() is supported only for unsharded"
                       " arrays.")
    return self._arrays[0].unsafe_buffer_pointer()

  @property
  @use_cpp_method()
  def __cuda_array_interface__(self):
    if len(self._arrays) != 1:
      raise ValueError("__cuda_array_interface__() is supported only for "
                       "unsharded arrays.")
    return self._arrays[0].__cuda_array_interface__  # pytype: disable=attribute-error  # bind-properties

  @use_cpp_method()
  def on_device_size_in_bytes(self):
    """Returns the total global on-device size of the array in bytes."""
    arr = self._arrays[0]
    per_shard_size = arr.on_device_size_in_bytes()  # type: ignore
    return per_shard_size * len(self.sharding.device_set)

  # TODO(yashkatariya): Remove this method when everyone is using devices().
  def device(self) -> Device:
    warnings.warn("arr.device() is deprecated. Use arr.devices() instead.",
                  DeprecationWarning, stacklevel=2)
    self._check_if_deleted()
    device_set = self.sharding.device_set
    if len(device_set) == 1:
      single_device, = device_set
      return single_device
    raise ValueError('Length of devices is greater than 1. '
                     'Please use `.devices()`.')

  def devices(self) -> set[Device]:
    self._check_if_deleted()
    return self.sharding.device_set

  # TODO(https://github.com/google/jax/issues/12380): Remove this when DA is
  # deleted.
  @property
  def device_buffer(self) -> ArrayImpl:
    # Added 2023 Dec 6
    warnings.warn(
      "arr.device_buffer is deprecated. Use arr.addressable_data(0)",
      DeprecationWarning, stacklevel=2)
    self._check_if_deleted()
    if len(self._arrays) == 1:
      return self._arrays[0]
    raise ValueError('Length of buffers is greater than 1. Please use '
                     '`.device_buffers` instead.')

  # TODO(https://github.com/google/jax/issues/12380): Remove this when SDA is
  # deleted.
  @property
  def device_buffers(self) -> Sequence[ArrayImpl]:
    # Added 2023 Dec 6
    warnings.warn(
      "arr.device_buffers is deprecated. Use [x.data for x in arr.addressable_shards]",
      DeprecationWarning, stacklevel=2)
    self._check_if_deleted()
    return cast(Sequence[ArrayImpl], self._arrays)

  def addressable_data(self, index: int) -> ArrayImpl:
    self._check_if_deleted()
    if self.is_fully_replicated:
      return self._fully_replicated_shard()
    return self._arrays[index]

  @functools.cached_property
  def addressable_shards(self) -> Sequence[Shard]:
    self._check_if_deleted()
    out = []
    for a in self._arrays:
      out.append(Shard(_get_device(a), self.sharding, self.shape, a))
    return out

  @property
  def global_shards(self) -> Sequence[Shard]:
    """Returns list of all `Shard`s of the Array across all devices.

    The result includes shards that are not addressable by the current process.
    If a `Shard` is not addressable, then its `data` will be `None`.
    """
    self._check_if_deleted()
    if self.is_fully_addressable:  # pylint: disable=using-constant-test
      return self.addressable_shards

    out = []
    device_id_to_buffer = {_get_device(a).id: a for a in self._arrays}
    for global_d in self.sharding.device_set:
      if device_id_to_buffer.get(global_d.id, None) is not None:
        array = device_id_to_buffer[global_d.id]
      else:
        array = None
      out.append(Shard(global_d, self.sharding, self.shape, array))
    return out

  @use_cpp_method()
  def delete(self):
    if self._arrays is None:
      return
    for buf in self._arrays:
      buf.delete()
    self._arrays = None
    self._npy_value = None

  @use_cpp_method()
  def is_deleted(self):
    if self._arrays is None:
      return True
    # This path is taken when a view of `Array` is created and the original
    # Array is deleted. In that case, the buffers the view represents also get
    # deleted.
    return any(buf.is_deleted() for buf in self._arrays)

  def _check_if_deleted(self):
    if self.is_deleted():
      raise RuntimeError(
          f"Array has been deleted with shape={self.aval.str_short()}.")

  @use_cpp_method()
  def block_until_ready(self):
    self._check_if_deleted()
    for db in self._arrays:
      db.block_until_ready()
    return self

  @use_cpp_method()
  def _single_device_array_to_np_array(self):
    return np.asarray(self._arrays[0])

  @use_cpp_method()
  def _copy_single_device_array_to_host_async(self):
    self._arrays[0].copy_to_host_async()

  @profiler.annotate_function
  def copy_to_host_async(self):
    self._check_if_deleted()
    if self._npy_value is None:
      if self.is_fully_replicated:
        self._copy_single_device_array_to_host_async()
        return
      copy_plan = _create_copy_plan(self._arrays, self.sharding, self.shape)
      for _, arr in copy_plan:
        arr._copy_single_device_array_to_host_async()

  @property
  @functools.partial(profiler.annotate_function, name="np.asarray(jax.Array)")
  def _value(self) -> np.ndarray:
    self._check_if_deleted()

    if self._npy_value is None:
      if self.is_fully_replicated:
        self._npy_value = self._single_device_array_to_np_array()  # type: ignore
        self._npy_value.flags.writeable = False
        return cast(np.ndarray, self._npy_value)

      # TODO(yashkatariya): Merge `_process_has_full_value_in_mcjax` with
      # is_fully_addressable.
      if (not self.is_fully_addressable and
          not _process_has_full_value_in_mcjax(self.sharding, self.shape)):
        raise RuntimeError("Fetching value for `jax.Array` that spans "
                           "non-addressable devices is not possible. You can use "
                           "`jax.experimental.multihost_utils.process_allgather` "
                           "for this use case.")

      copy_plan = _create_copy_plan(self._arrays, self.sharding, self.shape)
      for _, arr in copy_plan:
        arr._copy_single_device_array_to_host_async()

      npy_value = np.empty(self.shape, self.dtype)
      for ind, arr in copy_plan:
        npy_value[ind] = arr._single_device_array_to_np_array()
      self._npy_value = npy_value  # type: ignore
      self._npy_value.flags.writeable = False
    # https://docs.python.org/3/library/typing.html#typing.cast
    return cast(np.ndarray, self._npy_value)
