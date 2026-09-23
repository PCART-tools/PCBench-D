  def __init__(self, text: str, annotation: str | None = None):
    assert isinstance(text, str), text
    assert annotation is None or isinstance(annotation, str), annotation
    self.text = text
    self.annotation = annotation
