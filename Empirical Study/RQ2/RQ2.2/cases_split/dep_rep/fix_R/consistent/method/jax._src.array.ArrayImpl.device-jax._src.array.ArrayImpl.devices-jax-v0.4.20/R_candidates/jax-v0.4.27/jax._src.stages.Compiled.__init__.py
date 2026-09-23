  def __init__(self, executable, args_info, out_tree, no_kwargs=False):
    self._executable = executable
    self._no_kwargs = no_kwargs
    self.args_info = args_info
    self.out_tree = out_tree
    self._params = CompiledCallParams(self._executable, self._no_kwargs,
                                      self.in_tree, self.out_tree)
    self._call = None
