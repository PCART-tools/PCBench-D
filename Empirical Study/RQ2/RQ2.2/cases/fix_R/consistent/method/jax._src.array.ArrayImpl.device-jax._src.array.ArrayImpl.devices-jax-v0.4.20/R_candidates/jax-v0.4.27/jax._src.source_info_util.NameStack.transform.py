  def transform(self, transform_name: str) -> NameStack:
    return NameStack((*self.stack, Transform(transform_name)))
