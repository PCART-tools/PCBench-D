  def __init__(
      self,
      lowering: XlaLowering,
      args_info,  # PyTree of ArgInfo
      out_tree: tree_util.PyTreeDef,
      no_kwargs: bool = False):
    self._lowering = lowering
    self._no_kwargs = no_kwargs
    self.args_info = args_info
    self.out_tree = out_tree
