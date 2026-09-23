  def impl(self, fun, fwd, bwd, *args, out_trees):
    del fwd, bwd, out_trees
    with core.new_sublevel():
      return fun.call_wrapped(*args)
