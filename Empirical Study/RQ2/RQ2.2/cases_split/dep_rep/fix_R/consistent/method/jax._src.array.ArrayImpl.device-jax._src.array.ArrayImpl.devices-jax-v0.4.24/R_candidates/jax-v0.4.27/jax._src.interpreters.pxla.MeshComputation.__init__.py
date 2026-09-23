  def __init__(self, name: str, hlo: ir.Module | None,
               donated_invars: Sequence[bool], **compile_args):
    self._name = name
    self._hlo = hlo
    self._donated_invars = donated_invars
    self.compile_args = compile_args
    self._executable = None
