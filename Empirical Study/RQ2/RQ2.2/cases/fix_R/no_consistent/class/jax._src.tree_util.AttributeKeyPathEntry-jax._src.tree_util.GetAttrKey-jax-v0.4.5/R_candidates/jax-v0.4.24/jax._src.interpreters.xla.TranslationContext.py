@dataclasses.dataclass
class TranslationContext:
  builder: xc.XlaBuilder
  # TODO(phawkins): make platform non-optional. We should always be translating
  # with a specific platform in mind.
  platform: str | None
  axis_env: AxisEnv
  name_stack: str | source_info_util.NameStack

  def replace(self, **kw): return dataclasses.replace(self, **kw)
