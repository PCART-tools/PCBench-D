@tree_util.register_pytree_node_class
@dataclasses.dataclass(frozen=True)
class DebuggerFrame:
  """Encapsulates Python frame information."""
  filename: str
  locals: Dict[str, Any]
  code_context: str
  source: List[str]
  lineno: int
  offset: Optional[int]

  def tree_flatten(self):
    flat_locals, locals_tree = tree_util.tree_flatten(self.locals)
    is_valid = [
        isinstance(l, (core.Tracer, jnp.ndarray, np.ndarray))
        for l in flat_locals
    ]
    invalid_locals, valid_locals = util.partition_list(is_valid, flat_locals)
    return valid_locals, (is_valid, invalid_locals, locals_tree, self.filename,
                          self.code_context, self.source, self.lineno,
                          self.offset)

  @classmethod
  def tree_unflatten(cls, info, valid_locals):
    (is_valid, invalid_locals, locals_tree, filename, code_context, source,
     lineno, offset) = info
    flat_locals = util.merge_lists(is_valid, invalid_locals, valid_locals)
    locals_ = tree_util.tree_unflatten(locals_tree, flat_locals)
    return DebuggerFrame(filename, locals_, code_context, source, lineno,
                         offset)

  @classmethod
  def from_frameinfo(cls, frame_info) -> DebuggerFrame:
    try:
      _, start = inspect.getsourcelines(frame_info.frame)
      source = inspect.getsource(frame_info.frame).split('\n')
      offset = frame_info.lineno - start
    except OSError:
      source = []
      offset = None
    return DebuggerFrame(
        filename=frame_info.filename,
        locals=frame_info.frame.f_locals,
        code_context=frame_info.code_context,
        source=source,
        lineno=frame_info.lineno,
        offset=offset)
