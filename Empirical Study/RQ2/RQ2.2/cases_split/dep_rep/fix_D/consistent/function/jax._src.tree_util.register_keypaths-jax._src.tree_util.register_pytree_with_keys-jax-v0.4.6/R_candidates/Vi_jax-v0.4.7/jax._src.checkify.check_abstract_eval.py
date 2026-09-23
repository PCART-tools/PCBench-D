@check_p.def_effectful_abstract_eval
def check_abstract_eval(*args, err_tree, debug):
  del debug
  return [], set(tree_unflatten(err_tree, args)._pred.keys())
