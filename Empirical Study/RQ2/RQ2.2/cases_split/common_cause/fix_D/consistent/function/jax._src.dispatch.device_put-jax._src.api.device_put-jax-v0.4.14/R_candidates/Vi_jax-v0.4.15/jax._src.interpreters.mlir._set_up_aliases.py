def _set_up_aliases(avals_in, avals_out, donated_args, arg_memory_kinds,
                    result_memory_kinds):
  input_output_aliases = [None] * len(avals_in)
  # To match-up in-avals to out-avals we only care about the number of
  # bytes, so we strip off unrelated aval metadata (eg. the named shape)
  strip_metadata = lambda a: a.strip_named_shape().strip_weak_type()
  avals_in = map(strip_metadata, avals_in)
  avals_out = map(strip_metadata, avals_out)

  # Both arg and result memory kinds need to be specified to donate based on
  # the memory kind. For jit's where out_shardings is not specified, we don't
  # know the memory kind so don't condition the logic based on the memory kind.
  # TODO(yashkatariya): Note that this logic should be in C++ where we make
  # donation decisions are made after SPMD propagation passes and memory
  # placement passes so that we have all the information.
  if (arg_memory_kinds is None or result_memory_kinds is None or
      any(a is None for a in arg_memory_kinds) or
      any(r is None for r in result_memory_kinds)):
    arg_memory_kinds = [None] * len(avals_in)
    result_memory_kinds = [None] * len(avals_out)

  donations = collections.defaultdict(collections.deque)
  for i, (aval, am, donated) in enumerate(
      zip(avals_in, arg_memory_kinds, donated_args)):
    if donated:
      donations[(aval, am)].append(i)

  out_donated_args = list(donated_args)
  for i, (aval, rm) in enumerate(zip(avals_out, result_memory_kinds)):
    # Only donate if memory kinds match. Relax this when the compiler can
    # donate across memories.
    key = (aval, rm)
    if donations.get(key, ()):
      input_id = donations[key].popleft()
      input_output_aliases[input_id] = i
      out_donated_args[input_id] = False

  return input_output_aliases, out_donated_args
