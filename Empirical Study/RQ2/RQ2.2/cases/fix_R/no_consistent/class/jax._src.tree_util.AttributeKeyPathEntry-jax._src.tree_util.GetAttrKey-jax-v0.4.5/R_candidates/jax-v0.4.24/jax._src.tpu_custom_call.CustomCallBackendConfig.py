@dataclasses.dataclass(frozen=True)
class CustomCallBackendConfig:
  """Represents an unserialized backend config for custom calls."""
  lowered_module_asm: bytes
  has_communication: bool
  collective_id: int | None
  device_type: str | None
  cost_estimate: CostEstimate | None
  needs_hlo_passes: bool
  needs_layout_passes: bool
  vmem_limit_bytes: int | None
  flags: dict[str, bool | int | float] | None

  # We omit the body while printing, because primitive params get embedded
  # in HLO metadata, and the body blows up its size.
  def __repr__(self):
    return "CustomCallBackendConfig(<omitted>)"

  def to_json(self) -> bytes:
    """Serializes the backend config into JSON."""
    # We format the JSON ourselves, because json.dumps seems to be overly slow.
    config = io.BytesIO()
    config.write(b'{"custom_call_config": {"body": "')
    config.write(base64.b64encode(self.lowered_module_asm))
    config.write(b'"')
    if self.has_communication:
      config.write(b', "has_communication": ')
      config.write(str(self.has_communication).lower().encode("ascii"))
    if self.collective_id is not None:
      config.write(b', "collective_id": ')
      config.write(str(self.collective_id).encode("ascii"))
    if self.cost_estimate is not None:
      config.write(b', "cost_estimate": ')
      config.write(self.cost_estimate.to_json())
    if self.needs_hlo_passes:
      config.write(b', "needs_hlo_passes": ')
      config.write(str(self.needs_hlo_passes).lower().encode("ascii"))
    if self.needs_layout_passes:
      config.write(b', "needs_layout_passes": ')
      config.write(str(self.needs_layout_passes).lower().encode("ascii"))
    config.write(b"}")
    if self.device_type is not None:
      config.write(b', "device_type": ')
      config.write(
          ('"DEVICE_TYPE_' + self.device_type.upper() + '"').encode("ascii")
      )
    if self.vmem_limit_bytes is not None:
      config.write(
          b', "scoped_memory_configs": [{"memory_space":1, "offset": 0,'
          b' "size": '
      )
      config.write(str(self.vmem_limit_bytes).encode("ascii"))
      config.write(b'}]')
    if self.flags is not None:
      config.write(b', "flag_configs": [')
      for i, (flag, value) in enumerate(self.flags.items()):
        config.write(b'{"flag_type": "')
        config.write(flag.encode("ascii"))
        config.write(b'", value: {')
        if isinstance(value, bool):
          config.write(b'"boolean_value": ')
          config.write(b"true" if value else b"false")
        elif isinstance(value, int):
          config.write(b'"integer_value": ')
          config.write(str(value).encode("ascii"))
        elif isinstance(value, float):
          config.write(b'"double_value": ')
          config.write(str(value).encode("ascii"))
        else:
          raise ValueError("invalid flag value: " + str(value))
        config.write(b"}}")
        if i + 1 != len(self.flags):
          config.write(b",")
      config.write(b"]")
    config.write(b"}")
    return config.getvalue()
