@dataclasses.dataclass
class DeviceAssignmentMismatch:
  da: Sequence[xc.Device]
  m_type: MismatchType
  source_info: dispatch.SourceInfo | None

  @property
  def device_ids(self) -> Sequence[int]:
    return [d.id for d in self.da]

  @property
  def platform(self) -> str:
    return self.da[0].platform.upper()

  def _maybe_api_name(self, api_name) -> str:
    return f" {api_name}'s" if self.m_type == MismatchType.CONTEXT_DEVICES else ""

  @property
  def source_info_str(self):
    return "" if self.source_info is None else f" at {self.source_info.source_info}"

  @property
  def _dev_ids_plat_str(self):
    return f"device ids {self.device_ids} on platform {self.platform}"

  def m_type_str(self, api_name):
    return (f'{self.source_info and self.source_info.eqn_name} inside {api_name}'
            if self.m_type == MismatchType.SHARDING_INSIDE_COMPUTATION else self.m_type)

  def _str(self, api_name):
    return (f"{self._maybe_api_name(api_name)} {self.m_type_str(api_name)} with "
            f"{self._dev_ids_plat_str}{self.source_info_str}")
