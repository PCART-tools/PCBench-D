def flattened_fun_in_tree(
    fn: lu.WrappedFun
  ) -> Optional[tuple[PyTreeDef, Callable[[], PyTreeDef], bool]]:
  # This implementation relies on internal details of linear_util.py's
  # WrappedFun, but it's for the worthy cause of better user error messages.
  # It can fail (i.e. return None) if its WrappedFun argument is not transformed
  # with flatten_fun or flatten_fun_nokwargs, which could happen e.g. when
  # core.eval_jaxpr encounters a call primitive (though at that point we're just
  # round-tripping jaxprs and the user errors in question are impossible).
  assert isinstance(flatten_fun, partial) and len(flatten_fun.args) == 1
  assert (isinstance(flatten_fun_nokwargs, partial) and
          len(flatten_fun_nokwargs.args) == 1)
  flattens = {flatten_fun.args[0], flatten_fun_nokwargs.args[0]}
  try:
    ((in_tree,), out_tree_store, has_kwargs), = (
        (args, store, f is flatten_fun.args[0])
        for (f, args), store in zip(fn.transforms, fn.stores) if f in flattens)
  except ValueError:
    return None
  else:
    return in_tree, lambda: out_tree_store.val, has_kwargs
