  def tree_flatten(self):
    flat_locals, locals_tree = _safe_flatten_dict(self.locals)
    flat_globals, globals_tree = _safe_flatten_dict(self.globals)
    flat_vars = flat_locals + flat_globals
    is_valid = [isinstance(l, core.Tracer) for l in flat_vars]
    invalid_vars, valid_vars = util.partition_list(is_valid, flat_vars)
    return valid_vars, (is_valid, invalid_vars, locals_tree, globals_tree,
                        len(flat_locals), self.filename, self.code_context,
                        self.source, self.lineno, self.offset)
