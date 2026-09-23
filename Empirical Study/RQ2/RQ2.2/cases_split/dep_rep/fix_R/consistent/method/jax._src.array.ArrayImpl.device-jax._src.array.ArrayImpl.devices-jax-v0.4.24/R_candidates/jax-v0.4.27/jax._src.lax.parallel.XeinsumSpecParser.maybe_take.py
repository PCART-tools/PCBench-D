  def maybe_take(self, char: str, on_eof: bool = False):
    if self.eof:
      return on_eof
    if self.cur == char:
      self.pos += 1
      return True
