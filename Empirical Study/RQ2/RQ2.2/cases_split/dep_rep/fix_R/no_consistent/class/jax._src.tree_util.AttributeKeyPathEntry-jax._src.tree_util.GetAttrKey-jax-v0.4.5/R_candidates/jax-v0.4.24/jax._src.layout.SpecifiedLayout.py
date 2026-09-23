class SpecifiedLayout(XLACompatibleLayout):
  layout: xc.Layout

  def __init__(self, layout: xc.Layout):
    self._layout = layout
    self._layout_str = self._layout.to_string()
    self._minor_to_major = self._layout.minor_to_major()

  def __repr__(self):
    return f'SpecifiedLayout({self._layout_str})'

  def __hash__(self):
    return hash(self._layout)

  def __eq__(self, other):
    if not isinstance(other, SpecifiedLayout):
      return False
    return self._layout == other._layout

  def _to_xla_layout(self) -> str:
    return self._layout_str
