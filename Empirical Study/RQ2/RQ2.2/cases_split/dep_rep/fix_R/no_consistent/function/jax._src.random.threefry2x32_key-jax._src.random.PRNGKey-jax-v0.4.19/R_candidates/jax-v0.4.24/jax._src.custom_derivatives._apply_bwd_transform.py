def _apply_bwd_transform(todos, bwd):
  todos_list = list(todos)
  while todos_list:
    bwd = todos_list.pop()(bwd)
  return bwd
