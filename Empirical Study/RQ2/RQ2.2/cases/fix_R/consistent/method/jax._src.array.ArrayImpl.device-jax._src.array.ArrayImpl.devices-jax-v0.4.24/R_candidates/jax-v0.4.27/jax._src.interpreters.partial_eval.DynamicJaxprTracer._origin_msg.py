  def _origin_msg(self):
    if not self._trace.main.jaxpr_stack:  # type: ignore
      # If this Tracer has been leaked the jaxpr stack may no longer be
      # available. So we can't print as much origin information.
      return ("\nThis DynamicJaxprTracer was created on line "
              f"{source_info_util.summarize(self._line_info)}")
    else:
      invar_pos, progenitor_eqns = self._trace.frame.find_progenitors(self)
    dbg = self._debug_info
    if dbg is None:
      return ""

    origin = ("The error occurred while tracing the function "
              f"{dbg.func_src_info or '<unknown>'} for {dbg.traced_for}. ")
    arg_info = arg_info_all(dbg)
    if invar_pos and arg_info:
      arg_info = [arg_info[i] for i in invar_pos]
      arg_names = [f'{name}{keystr(path)}' for name, path in arg_info]
      if len(arg_names) == 1:
        arg_info_str = f"the argument {arg_names[0]}"
      elif len(arg_names) == 2:
        arg_info_str = f"the arguments {arg_names[0]} and {arg_names[1]}"
      else:
        *rest, last = arg_names
        arg_info_str = f"the arguments {', '.join(rest)}, and {last}"
      origin += ("This concrete value was not available in Python because it "
                 f"depends on the value{'s' if len(invar_pos) > 1 else ''} "
                 f"of {arg_info_str}.")
    elif progenitor_eqns:
      msts = ["  operation "
              f"{core.pp_eqn(eqn, core.JaxprPpContext(), core.JaxprPpSettings(print_shapes=True))}\n"
              f"    from line {source_info_util.summarize(eqn.source_info)}"
              for eqn in progenitor_eqns[:5]]  # show at most 5
      origin += ("This value became a tracer due to JAX operations on these lines:"
                 "\n\n" + "\n\n".join(msts))
      if len(progenitor_eqns) > 5:
        origin += "\n\n(Additional originating lines are not shown.)"
    return "\n" + origin
