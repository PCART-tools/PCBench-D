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
