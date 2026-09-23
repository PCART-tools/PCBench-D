class _ColorDoc(Doc):
  __slots__ = ("foreground", "background", "intensity", "child")
  foreground: Optional[Color]
  background: Optional[Color]
  intensity: Optional[Intensity]
  child: Doc

  def __init__(self, child: Doc, *, foreground: Optional[Color] = None,
               background: Optional[Color] = None,
               intensity: Optional[Intensity] = None):
    assert isinstance(child, Doc), child
    self.child = child
    self.foreground = foreground
    self.background = background
    self.intensity = intensity
