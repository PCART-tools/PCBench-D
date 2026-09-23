  @profiler.annotate_function
  def call(self, *args):
    # TODO(frostig): do we need to check sharding and sharded avals?
    arg_avals = map(xla.abstractify, args)
    check_arg_avals_for_call(self.in_avals, arg_avals, self._jaxpr_debug_info)
    return self.unsafe_call(*args)  # pylint: disable=not-callable
