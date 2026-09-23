  def __init__(self, child: Doc, *, foreground: Color | None = None,
               background: Color | None = None,
               intensity: Intensity | None = None):
    assert isinstance(child, Doc), child
    self.child = child
    self.foreground = foreground
    self.background = background
    self.intensity = intensity
