@util.curry
def transformation_with_aux(
    gen, fun: lu.WrappedFun, *gen_static_args) -> Tuple[lu.WrappedFun, Any]:
  out_store = StoreEqual()
  out_thunk = lambda: out_store.val
  return fun.wrap(gen, gen_static_args, out_store), out_thunk
