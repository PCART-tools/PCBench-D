  @classmethod
  def tree_unflatten(cls, info, valid_vars):
    (is_valid, invalid_vars, locals_tree, globals_tree, num_locals, filename,
     code_context, source, lineno, offset) = info
    flat_vars = util.merge_lists(is_valid, invalid_vars, valid_vars)
    flat_locals, flat_globals = util.split_list(flat_vars, [num_locals])
    locals_ = tree_util.tree_unflatten(locals_tree, flat_locals).to_dict()
    globals_ = tree_util.tree_unflatten(globals_tree, flat_globals).to_dict()
    return DebuggerFrame(filename, locals_, globals_, code_context, source,
                         lineno, offset)
