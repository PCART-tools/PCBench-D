  @classmethod
  def from_flat_info(cls,
                     lowering: XlaLowering,
                     in_tree: tree_util.PyTreeDef,
                     in_avals,
                     donate_argnums: tuple[int, ...],
                     out_tree: tree_util.PyTreeDef,
                     no_kwargs: bool = False):
    """Initialize from flat info (``in_avals`` etc.) and an input PyTreeDef.

    Args:
      in_tree: The ``PyTreeDef`` of (args, kwargs).
      out_tree: The ``PyTreeDef`` of the outputs.
      no_kwargs: If ``True`` the transformation, and the
        ``Compiled`` returned from this object will not support keyword
        arguments (an error will be raised if some are provided).
    """
    return cls(
        lowering,
        make_args_info(in_tree, in_avals, donate_argnums),
        out_tree,
        no_kwargs=no_kwargs)
