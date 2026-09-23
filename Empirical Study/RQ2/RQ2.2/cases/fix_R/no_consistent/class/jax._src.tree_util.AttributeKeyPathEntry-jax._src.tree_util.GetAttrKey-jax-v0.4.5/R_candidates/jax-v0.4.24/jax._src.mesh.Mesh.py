class Mesh(contextlib.ContextDecorator):
  """Declare the hardware resources available in the scope of this manager.

  In particular, all ``axis_names`` become valid resource names inside the
  managed block and can be used e.g. in the ``in_axis_resources`` argument of
  :py:func:`jax.experimental.pjit.pjit`. Also see JAX's multi-process programming
  model (https://jax.readthedocs.io/en/latest/multi_process.html)
  and the Distributed arrays and automatic parallelization tutorial
  (https://jax.readthedocs.io/en/latest/notebooks/Distributed_arrays_and_automatic_parallelization.html)

  If you are compiling in multiple threads, make sure that the
  ``with Mesh`` context manager is inside the function that the threads will
  execute.

  Args:
    devices: A NumPy ndarray object containing JAX device objects (as
      obtained e.g. from :py:func:`jax.devices`).
    axis_names: A sequence of resource axis names to be assigned to the
      dimensions of the ``devices`` argument. Its length should match the
      rank of ``devices``.

  Example:

    >>> from jax.experimental.pjit import pjit
    >>> from jax.sharding import Mesh
    >>> from jax.sharding import PartitionSpec as P
    >>> import numpy as np
    ...
    >>> inp = np.arange(16).reshape((8, 2))
    >>> devices = np.array(jax.devices()).reshape(4, 2)
    ...
    >>> # Declare a 2D mesh with axes `x` and `y`.
    >>> global_mesh = Mesh(devices, ('x', 'y'))
    >>> # Use the mesh object directly as a context manager.
    >>> with global_mesh:
    ...   out = pjit(lambda x: x, in_shardings=None, out_shardings=None)(inp)

    >>> # Initialize the Mesh and use the mesh as the context manager.
    >>> with Mesh(devices, ('x', 'y')) as global_mesh:
    ...   out = pjit(lambda x: x, in_shardings=None, out_shardings=None)(inp)

    >>> # Also you can use it as `with ... as ...`.
    >>> global_mesh = Mesh(devices, ('x', 'y'))
    >>> with global_mesh as m:
    ...   out = pjit(lambda x: x, in_shardings=None, out_shardings=None)(inp)

    >>> # You can also use it as `with Mesh(...)`.
    >>> with Mesh(devices, ('x', 'y')):
    ...   out = pjit(lambda x: x, in_shardings=None, out_shardings=None)(inp)
  """

  devices: np.ndarray
  axis_names: tuple[MeshAxisName, ...]

  def __new__(cls, devices: np.ndarray | Sequence[xc.Device],
              axis_names: str | Sequence[MeshAxisName]):
    if not isinstance(devices, np.ndarray):
      devices = np.array(devices)
    if isinstance(axis_names, str):
      axis_names = (axis_names,)
    axis_names = tuple(axis_names)

    if devices.ndim != len(axis_names):
      raise ValueError(
          "Mesh requires the ndim of its first argument (`devices`) to equal "
          "the length of its second argument (`axis_names`), but got "
          f"devices.ndim == {devices.ndim} and "
          f"len(axis_names) == {len(axis_names)}.")

    key = (axis_names, devices.shape, tuple(devices.flat))
    val = _mesh_object_dict.get(key, None)
    if val is not None:
      return val

    self = super().__new__(cls)
    self.devices = devices.copy()
    self.devices.flags.writeable = False
    self.axis_names = axis_names
    _mesh_object_dict[key] = self
    return self

  def __reduce__(self):
    return (type(self), (self.devices, self.axis_names))

  def __eq__(self, other):
    if not isinstance(other, Mesh):
      return False
    # This is a performance optimization. Comparing thousands of devices
    # can be expensive.
    if id(self) == id(other):
      return True
    return (self.axis_names == other.axis_names and
            self.devices.shape == other.devices.shape and
            self._internal_device_list == other._internal_device_list)

  def __hash__(self):
    if not hasattr(self, '_hash'):
      self._hash = hash(
          (self.axis_names, self._internal_device_list, self.devices.shape))
    return self._hash

  def __setattr__(self, name, value):
    if hasattr(self, name):
      if getattr(self, name) == value:
        # This can to happen if two threads race, for example if two threads
        # are trying to hash the same Mesh instance.
        return
      raise RuntimeError(
          f"Cannot reassign attributes ({name}) of immutable mesh objects"
      )
    super().__setattr__(name, value)

  def __enter__(self):
    new_env = thread_resources.stack[-1].with_mesh(self)
    thread_resources.stack.append(new_env)
    thread_resources.env = new_env
    jax_config.update_thread_local_jit_state(
        mesh_context_manager=tuple(t.physical_mesh for t in thread_resources.stack
                                   if not t.physical_mesh.empty))
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    thread_resources.stack.pop()
    thread_resources.env = thread_resources.stack[-1]
    jax_config.update_thread_local_jit_state(
        mesh_context_manager=tuple(t.physical_mesh for t in thread_resources.stack
                                   if not t.physical_mesh.empty))
    return False

  @property
  def shape(self):
    return collections.OrderedDict(
        (name, size)
        for name, size in util.safe_zip(self.axis_names, self.devices.shape))

  @property
  def size(self):
    return math.prod(self.shape.values())

  @property
  def empty(self):
    return self.devices.ndim == 0

  @functools.cached_property
  def is_multi_process(self):
    return self.devices.size != len(self.local_devices)

  @property
  def local_mesh(self):
    return self._local_mesh(xb.process_index())

  def _local_mesh(self, process_index):
    return _get_local_mesh(self, process_index)

  @functools.cached_property
  def device_ids(self):
    assert not self.empty
    return np.vectorize(lambda d: d.id, otypes=[int])(self.devices)

  @functools.cached_property
  def _local_devices_set(self):
    return set(self.local_devices)

  @functools.cached_property
  def _flat_devices_tuple(self):
    return tuple(self.devices.flat)

  @functools.cached_property
  def _internal_device_list(self):
    return xc.DeviceList(self._flat_devices_tuple)

  @functools.cached_property
  def _flat_devices_set(self):
    return set(self.devices.flat)

  def __str__(self):
    mesh_str = ", ".join(f"'{k}': {v}" for k, v in self.shape.items())
    return f"Mesh({mesh_str})"

  @functools.cached_property
  def _repr(self):
    if self.empty:
      return "Mesh(device_ids=[], axis_names=())"
    return f"Mesh(device_ids={self.device_ids!r}, axis_names={self.axis_names!r})"

  def __repr__(self):
    return self._repr

  @functools.cached_property
  def local_devices(self):
    return [d for d in self.devices.flat
            if d.process_index == d.client.process_index()]
