def _apply_todos(todos, outs):
  todos_list = list(todos)
  while todos_list:
    outs = map(core.full_lower, todos_list.pop()(outs))
  return outs
