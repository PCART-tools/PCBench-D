def new_name_stack(name: str = ''):
  if config.jax_experimental_name_stack:
    from jax._src import source_info_util
    name_stack = source_info_util.NameStack()
    if name:
      name_stack = name_stack.extend(name)
    return name_stack
  return name + '/'
