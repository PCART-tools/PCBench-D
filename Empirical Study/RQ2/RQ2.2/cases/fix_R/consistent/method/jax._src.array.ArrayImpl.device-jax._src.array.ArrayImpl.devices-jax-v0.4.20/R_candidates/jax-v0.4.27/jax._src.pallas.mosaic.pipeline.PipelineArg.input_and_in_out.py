  @property
  def input_and_in_out(self) -> T:
    return cast(Any, self.input) + cast(Any, self.in_out)
