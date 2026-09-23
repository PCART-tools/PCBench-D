  def call(self, *args):
    args_after_dce = [a for i, a in enumerate(args) if i in self._kept_var_idx]
    if self._all_args_info is None:
      kept_args = args_after_dce
      ref_avals = self.in_avals
      debug_info = None
    else:
      kept_args = args
      ref_avals = self._all_args_info.in_avals
      debug_info = self._all_args_info.debug_info

    all_arg_avals = map(xla.abstractify, kept_args)
    check_arg_avals_for_call(ref_avals, all_arg_avals, debug_info)
    # Check the GDA sharding and the input sharding.
    check_array_xla_sharding_layout_match(
        args_after_dce, self._in_shardings, self._in_layouts, debug_info,
        self._kept_var_idx)
    return self.unsafe_call(*args)  # pylint: disable=not-callable
