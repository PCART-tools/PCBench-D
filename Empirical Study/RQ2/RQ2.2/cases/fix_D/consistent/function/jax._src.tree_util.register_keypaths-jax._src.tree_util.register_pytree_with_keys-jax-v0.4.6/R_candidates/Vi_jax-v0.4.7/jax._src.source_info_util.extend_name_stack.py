@contextlib.contextmanager
def extend_name_stack(name: str) -> Iterator[NameStack]:
  prev_context = _source_info_context.context
  curr_name_stack = prev_context.name_stack
  new_context = prev_context.replace(name_stack=curr_name_stack.extend(name))
  _source_info_context.context = new_context
  try:
    yield _source_info_context.context.name_stack
  finally:
    _source_info_context.context = prev_context
