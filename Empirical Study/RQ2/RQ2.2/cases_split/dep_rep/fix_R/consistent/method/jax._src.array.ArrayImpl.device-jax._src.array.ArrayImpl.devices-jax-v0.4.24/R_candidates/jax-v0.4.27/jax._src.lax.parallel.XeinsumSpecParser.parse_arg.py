  def parse_arg(self):
    subscripts = []
    names = []
    while not self.eof:
      subscript, cont = self.parse_subscript()
      if not cont: break
      subscripts.append(subscript)
    if self.eof:
      return False, (subscripts, names)
    if self.maybe_take(','):
      return True, (subscripts, names)
    else:
      assert self.maybe_take('{')
      first = True
      while not self.maybe_take('}'):
        if not first:
          assert self.maybe_take(',')
        first = False
        if self.eof:
          raise ValueError("Unterminated named axis brace")
        axis_name = self.parse_axis_name()
        names.append(axis_name)
      return self.maybe_take(',', False), (subscripts, names)
