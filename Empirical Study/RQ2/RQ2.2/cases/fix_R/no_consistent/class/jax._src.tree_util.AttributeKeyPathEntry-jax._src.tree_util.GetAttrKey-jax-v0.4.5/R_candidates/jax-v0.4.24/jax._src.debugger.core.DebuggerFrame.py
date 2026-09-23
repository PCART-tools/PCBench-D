@tree_util.register_pytree_node_class
@dataclasses.dataclass(frozen=True)
class DebuggerFrame:
  """Encapsulates Python frame information."""
  filename: str
  locals: dict[str, Any]
  globals: dict[str, Any]
  code_context: str
  source: list[str]
  lineno: int
  offset: int | None

  def tree_flatten(self):
    flat_locals, locals_tree = _safe_flatten_dict(self.locals)
    flat_globals, globals_tree = _safe_flatten_dict(self.globals)
    flat_vars = flat_locals + flat_globals
    is_valid = [isinstance(l, core.Tracer) for l in flat_vars]
    invalid_vars, valid_vars = util.partition_list(is_valid, flat_vars)
    return valid_vars, (is_valid, invalid_vars, locals_tree, globals_tree,
                        len(flat_locals), self.filename, self.code_context,
                        self.source, self.lineno, self.offset)

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

  @classmethod
  def from_frameinfo(cls, frame_info) -> DebuggerFrame:
    try:
      _, start = inspect.getsourcelines(frame_info.frame)
      source = inspect.getsource(frame_info.frame).split("\n")
      # Line numbers begin at 1 but offsets begin at 0. `inspect.getsource` will
      # return a partial view of the file and a `start` indicating the line
      # number that the source code starts at. However, it's possible that
      # `start` is 0, indicating that we are at the beginning of the file. In
      # this case, `offset` is just the `lineno - 1`. If `start` is nonzero,
      # then we subtract it off from the `lineno` and don't need to subtract 1
      # since both start and lineno are 1-indexed.
      offset = frame_info.lineno - max(start, 1)
    except OSError:
      source = []
      offset = None
    return DebuggerFrame(
        filename=frame_info.filename,
        locals=frame_info.frame.f_locals,
        globals={},
        code_context=frame_info.code_context,
        source=source,
        lineno=frame_info.lineno,
        offset=offset)
