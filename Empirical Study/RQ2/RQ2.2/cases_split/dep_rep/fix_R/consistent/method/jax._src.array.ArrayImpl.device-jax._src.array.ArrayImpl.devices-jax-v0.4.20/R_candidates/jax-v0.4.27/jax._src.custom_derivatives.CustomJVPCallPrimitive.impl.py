  def impl(self, fun, _, *args):
    with core.new_sublevel():
      return fun.call_wrapped(*args)
