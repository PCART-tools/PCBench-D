class Limitation:
  """Encodes conditions under which a harness is limited, e.g., not runnable in JAX.

  See the module docstring for an introduction to harnesses and limitations.
  """

  def __init__(
      self,
      description: str,
      *,
      enabled: bool = True,
      devices: str | Sequence[str] = ("cpu", "gpu", "tpu"),
      dtypes: Sequence[DType] = (),
      skip_run: bool = False,
  ):
    """Args:

      description: text to augment the harness group name with the description
      of the limitation. Used for reports.
      enabled: whether this limitation is enabled for the harness in which
        it appears. This is only used during testing to know whether to ignore
        harness errors. Use this sparingly, prefer `devices` and
        `dtypes` for enabled conditions that are included in reports.
      devices: a device type (string) or a sequence of device types
        for which this applies. By default, it applies to all devices types.
        Used for filtering during harness execution, and for reports.
      dtypes: the sequence of dtypes for which this applies. An empty sequence
        denotes all dtypes. Used for filtering during harness execution, and
        for reports.
      skip_run: this harness should not even be invoked (typically because it
        results in a crash). This should be rare.
    """
    assert isinstance(description, str), f"{description}"
    self.description = description
    self.skip_run = skip_run
    if isinstance(devices, str):
      devices = (devices,)
    else:
      devices = tuple(devices)
    self.devices = devices
    assert isinstance(dtypes, Iterable)
    dtypes = tuple(dtypes)
    self.dtypes = dtypes
    self.enabled = enabled  # Does it apply to the current harness?

  def __str__(self):
    return (f"\"{self.description}\" devices={self.devices} "
            f"dtypes={[np.dtype(dt).name for dt in self.dtypes]}" +
            (" (skip_run) " if self.skip_run else ""))

  __repr__ = __str__

  def filter(self,
             device: str | None = None,
             dtype: DType | None = None) -> bool:
    """Check that a limitation is enabled for the given dtype and device."""
    return (self.enabled and
            (not self.dtypes or dtype is None or dtype in self.dtypes) and
            (device is None or device in self.devices))
