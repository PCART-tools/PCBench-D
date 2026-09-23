  def parse_args(self):
    arg_specs = []
    cont = True
    while not self.eof:
      cont, result = self.parse_arg()
      arg_specs.append(result)
    if cont:
      arg_specs.append(([], []))
    return arg_specs
