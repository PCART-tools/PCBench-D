  def __init__(self, hlo: ir.Module, **compile_args):
    self._executable = None
    self._hlo = hlo
    self.compile_args = compile_args
