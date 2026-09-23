def explain_tracing_cache_miss(
    f: Callable, unseen_f: bool, cache: dict, key: tuple, result: tuple):
  if config.check_tracer_leaks.value: return

  def unpack(key):
    transforms, (), _, (in_type, debug_info, _, inline), *_, ctx = key
    (_, (in_tree,)), (_, ()) = transforms
    return in_tree, in_type, debug_info, inline.val, ctx
  in_tree, in_type, debug_info, inline, ctx = unpack(key)
  if inline: return

  msg: list[str] = []
  p = msg.append
  done = lambda: logger.log(logging.WARNING, '\n'.join(msg))

  callsite = source_info_util.summarize(source_info_util.current())
  p(f"TRACING CACHE MISS at {callsite} because:")

  # have we seen this function before at all?
  fun_name = getattr(f, '__qualname__', f)
  if debug_info.func_src_info:
    _, _, *rest = debug_info.func_src_info.split(' ')
    src_info = " defined at "  + ' '.join(rest)
  else:
    src_info = ''
  if unseen_f:
    p(f"  never seen function:\n    {fun_name} id={id(f)}{src_info}")
    if callsite in callsites:
      p("  but seen another function defined on the same line; maybe the function is\n"
        "  being re-defined repeatedly, preventing caching?")
    callsites.add(callsite)
    return done()
  else:
    p(f"  for {fun_name}{src_info}")

  seen_keys = map(unpack, cache.keys())

  # have we maybe switched some args to be kwargs or visa-versa?
  args_tree, kwargs_tree = treedef_children(in_tree)
  args_kwargs_trees = [treedef_children(k) for k, *_ in seen_keys]
  args_kwargs_match = [t for t in args_kwargs_trees
                       if t == [args_tree, kwargs_tree]]
  if not args_kwargs_match:
    num_args = len(treedef_children(args_tree))
    _, kwarg_keys = kwargs_tree.node_data()  # type: ignore
    p(f"  never seen passing {num_args} positional args and {len(kwarg_keys)} "
      "keyword args with keys:\n"
      f"    {', '.join(map(repr, kwarg_keys))}")
    dont_match = [set(t[1].node_data()[1]) for t in args_kwargs_trees  # type: ignore
                  if t != [args_tree, kwargs_tree]]
    close_kwargs = min(dont_match, key=set(kwarg_keys).symmetric_difference)
    if not close_kwargs:
      p("  closest seen is passing no keyword args")
    else:
      p(f"  closest seen passes {len(close_kwargs)} keyword args with keys:\n"
        f"    {', '.join(map(repr, close_kwargs))}")
    return done()

  # have we never seen this tracing context before?
  ctxs_match = [c for *_, c in seen_keys if c == ctx]
  if not ctxs_match:
    p("  tracing context doesn't match, e.g. due to config or context manager")
    dont_match = [c for *_, c in seen_keys if c != ctx]
    closest_ctx = min(dont_match, key=lambda c: sum(map(op.ne, c, ctx)))
    idxs = [i for i, (c1, c2) in enumerate(zip(ctx, closest_ctx)) if c1 != c2]
    p("  closest seen context tuple differs at positions:\n"
      f"    {', '.join(map(str, idxs))}\n"
      "  compare to tuple returned by config._trace_context() in jax/_src/config.py.")
    return done()

  # have we never seen this input pytree before?
  trees_match = [k for k in seen_keys if k[0] == in_tree]
  if not trees_match:
    in_tree_str = f':\n    {in_tree}' if len(str(in_tree)) < 76 else ''
    p(f"  never seen input pytree{in_tree_str}")
    dont_match = [t for t, *_ in seen_keys if t != in_tree]
    closest_tree = min(dont_match, key=lambda t: abs(t.num_leaves - in_tree.num_leaves))
    # TODO(mattjj): make equality_errors not print type name, avoid metaclass
    leaf = type('LeafMeta', (type,), dict(__repr__=lambda _: 'leaf'))('Leaf', (), {})()
    this_dummy = tree_unflatten(in_tree, [leaf] * in_tree.num_leaves)
    close_dummy = tree_unflatten(closest_tree, [leaf] * closest_tree.num_leaves)  # type: ignore
    errs = list(tree_util.equality_errors(this_dummy, close_dummy))
    p(f"  closest seen input pytree has {len(errs)} mismatches, including:")
    for path, thing1, thing2, explanation in errs:
      fst, *path = path  # type: ignore
      base = ['args', 'kwargs'][fst.idx]
      p(f"    * at {base}{keystr(path)}, seen {thing2} but now given {thing1},"  # type: ignore
        f"      so {explanation}")
    return done()

  # have we never seen these input types (eg shapes, dtypes) before?
  types_match = [k for k in trees_match if k[1] == in_type]
  if not types_match:
    if len(in_type) < 5:
      in_type_str = ':\n    {}'.format(',  '.join(
          f'{n}: {ty.str_short(short_dtypes=True)}'
          for n, ty in zip(debug_info.arg_names, in_type)))
    else:
      in_type_str = ''
    p(f"  never seen input type signature{in_type_str}")
    dont_match = [t for _, t, *_ in trees_match if t != in_type]
    closest_ty = min(dont_match, key=lambda t: sum(map(op.ne, t, in_type)))
    num_mismatch = sum(map(op.ne, closest_ty, in_type))
    p(f"  closest seen input type signature has {num_mismatch} mismatches, including:")
    add_weak_type_hint = False
    for name, ty1, ty2 in zip(debug_info.arg_names, closest_ty, in_type):
      if ty1 != ty2:
        if type(ty1) == type(ty2) == core.ShapedArray:
          s1, s2 = ty1.str_short(True), ty2.str_short(True)
          if s1 == s2:  # weak types don't show up in str_short()
            assert ty1.weak_type ^ ty2.weak_type
            s1 += f'{{weak_type={ty1.weak_type}}}'
            s2 += f'{{weak_type={ty2.weak_type}}}'
            add_weak_type_hint = True
        else:
          s1, s2 = str(ty1), str(ty2)
        p(f"    * at {name}, seen {s1}, but now given {s2}")
    if add_weak_type_hint:
      p('where weak_type=True often means a Python builtin numeric value, and ')
      p('weak_type=False means a jax.Array.')
      p('See https://jax.readthedocs.io/en/latest/type_promotion.html#weak-types')
    return done()

  # we think this is unreachable...
  p("explanation unavailable! please open an issue at https://github.com/google/jax")
  return done()
