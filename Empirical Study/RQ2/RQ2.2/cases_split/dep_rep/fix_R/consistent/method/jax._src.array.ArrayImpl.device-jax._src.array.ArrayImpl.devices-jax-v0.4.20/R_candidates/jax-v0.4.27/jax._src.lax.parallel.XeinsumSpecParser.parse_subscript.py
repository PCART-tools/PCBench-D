  def parse_subscript(self):
    if self.cur in string.ascii_lowercase:
      out = self.cur
      self.pos += 1
      return out, True
    else:
      return None, False
