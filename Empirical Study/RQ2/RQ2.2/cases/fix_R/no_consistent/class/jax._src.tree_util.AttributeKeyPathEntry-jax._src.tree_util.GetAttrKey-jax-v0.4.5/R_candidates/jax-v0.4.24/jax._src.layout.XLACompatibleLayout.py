class XLACompatibleLayout(Layout):

  def _to_xla_layout(self) -> str:
    raise NotImplementedError("Subclasses should implement this method.")
