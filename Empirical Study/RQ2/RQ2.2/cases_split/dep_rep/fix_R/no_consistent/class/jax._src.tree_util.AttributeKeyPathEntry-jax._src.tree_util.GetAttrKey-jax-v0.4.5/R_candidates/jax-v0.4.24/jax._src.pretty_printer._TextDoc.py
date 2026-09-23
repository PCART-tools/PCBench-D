class _TextDoc(Doc):
  __slots__ = ("text", "annotation")
  text: str
  annotation: str | None

  def __init__(self, text: str, annotation: str | None = None):
    assert isinstance(text, str), text
    assert annotation is None or isinstance(annotation, str), annotation
    self.text = text
    self.annotation = annotation

  def __repr__(self):
    if self.annotation is not None:
      return f"text(\"{self.text}\", annotation=\"{self.annotation}\")"
    else:
      return f"text(\"{self.text}\")"
