def _check_scan_carry_type(body_fun, in_carry, out_carry_tree, out_avals):
  try:
    sig = inspect.signature(body_fun)
  except (ValueError, TypeError):
    sig = None
  carry_name = sig and list(sig.parameters)[0]
  if carry_name:
    component = lambda p: (f'the input carry component {carry_name}{keystr(p)}'
                           if p else f'the input carry {carry_name}')
  else:
    component = lambda p: (f'the input carry at path {keystr(p)}'
                           if p else 'the input carry')
  leaves_and_paths, in_carry_tree = tree_flatten_with_path(in_carry)
  paths, in_carry_flat = unzip2(leaves_and_paths)
  in_avals = _map(_abstractify, in_carry_flat)
  if in_carry_tree != out_carry_tree:
    try:
      out_carry = tree_unflatten(out_carry_tree, out_avals)
    except:
      out_carry = None

    if out_carry is None:
      differences = [f'the input tree structure is:\n{in_carry_tree}\n',
                     f'the output tree structure is:\n{out_carry_tree}\n']
    else:
      differences = '\n'.join(
          f'  * {component(path)} is a {thing1} but the corresponding component '
          f'of the carry output is a {thing2}, so {explanation}\n'
          for path, thing1, thing2, explanation
          in equality_errors(in_carry, out_carry))
    raise TypeError(
        "Scanned function carry input and carry output must have the same "
        "pytree structure, but they differ:\n"
        f"{differences}\n"
        "Revise the scanned function so that its output is a pair where the "
        "first element has the same pytree structure as the first argument."
    )
  if not all(_map(core.typematch, in_avals, out_avals)):
    differences = '\n'.join(
        f'  * {component(path)} has type {in_aval.str_short()}'
        ' but the corresponding output carry component has type '
        f'{out_aval.str_short()}{_aval_mismatch_extra(in_aval, out_aval)}\n'
        for path, in_aval, out_aval in zip(paths, in_avals, out_avals)
        if not core.typematch(in_aval, out_aval))
    raise TypeError(
        "Scanned function carry input and carry output must have equal types "
        "(e.g. shapes and dtypes of arrays), "
        "but they differ:\n"
        f"{differences}\n"
        "Revise the scanned function so that all output types (e.g. shapes "
        "and dtypes) match the corresponding input types."
    )
