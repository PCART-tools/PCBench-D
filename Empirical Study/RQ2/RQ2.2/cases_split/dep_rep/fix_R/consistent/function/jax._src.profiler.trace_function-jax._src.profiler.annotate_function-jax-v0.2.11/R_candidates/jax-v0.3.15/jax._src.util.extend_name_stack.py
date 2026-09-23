def extend_name_stack(stack, name: str):
  if config.jax_experimental_name_stack:
    from jax._src import source_info_util
    assert isinstance(stack, source_info_util.NameStack), stack
    return stack.extend(name)
  assert isinstance(stack, str)
  return stack + name + '/'
