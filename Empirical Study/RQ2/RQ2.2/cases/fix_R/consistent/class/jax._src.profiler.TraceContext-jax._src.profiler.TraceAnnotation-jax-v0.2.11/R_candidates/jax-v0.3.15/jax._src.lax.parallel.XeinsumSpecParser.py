class XeinsumSpecParser:
  spec: str
  pos: int

  def __init__(self, spec: str):
    self.spec = spec
    self.pos = 0

  @property
  def eof(self):
    return self.pos == len(self.spec)

  @property
  def cur(self):
    return self.spec[self.pos]

  def parse_subscript(self):
    if self.cur in string.ascii_lowercase:
      out = self.cur
      self.pos += 1
      return out, True
    else:
      return None, False

  def parse_axis_name(self):
    try:
      end = self.spec.index('}', self.pos)
    except ValueError:
      assert False

    try:
      end = self.spec.index(',', self.pos, end)
    except ValueError:
      pass

    axis_name = self.spec[self.pos:end]
    assert axis_name
    self.pos = end
    return axis_name

  def maybe_take(self, char: str, on_eof: bool = False):
    if self.eof:
      return on_eof
    if self.cur == char:
      self.pos += 1
      return True

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

  def parse_args(self):
    arg_specs = []
    cont = True
    while not self.eof:
      cont, result = self.parse_arg()
      arg_specs.append(result)
    if cont:
      arg_specs.append(([], []))
    return arg_specs
