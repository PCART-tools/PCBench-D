@contextlib.contextmanager
def set_name_stack(name_stack: NameStack) -> Iterator[None]:
  prev_context = _source_info_context.context
  new_context = prev_context.replace(name_stack=name_stack)
  _source_info_context.context = new_context
  try:
    yield
  finally:
    _source_info_context.context = prev_context
