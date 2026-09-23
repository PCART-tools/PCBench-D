  def __repr__(self):
    if self.annotation is not None:
      return f"text(\"{self.text}\", annotation=\"{self.annotation}\")"
    else:
      return f"text(\"{self.text}\")"
