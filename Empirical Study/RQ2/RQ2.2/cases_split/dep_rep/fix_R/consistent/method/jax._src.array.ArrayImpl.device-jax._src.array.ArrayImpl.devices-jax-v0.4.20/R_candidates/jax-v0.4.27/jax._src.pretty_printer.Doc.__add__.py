  def __add__(self, other: Doc) -> Doc:
    return concat([self, other])
