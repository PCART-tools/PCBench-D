@custom_api_util.register_custom_decorator_type
class custom_vmap:
  fun: Callable
  vmap_rule: Callable | None

  def __init__(self, fun: Callable):
    functools.update_wrapper(self, fun)
    self.fun = fun  # type: ignore[assignment]
    self.vmap_rule = None

  __getattr__ = custom_api_util.forward_attr

  def def_vmap(self, vmap_rule: Callable) -> Callable:
    self.vmap_rule = vmap_rule
    return vmap_rule

  @traceback_util.api_boundary
  def __call__(self, *args, **kwargs):
    assert not kwargs
    args_flat, in_tree = tree_flatten(args)
    flat_fun, out_tree = flatten_fun_nokwargs(lu.wrap_init(self.fun), in_tree)
    in_avals = [core.raise_to_shaped(core.get_aval(x)) for x in args_flat]
    debug = pe.debug_info(self.fun, in_tree, out_tree, False, "custom_vmap")
    jaxpr, _, consts, () = pe.trace_to_jaxpr_dynamic(flat_fun, in_avals, debug)
    closed_call = core.ClosedJaxpr(pe.convert_constvars_jaxpr(jaxpr), ())
    in_tree = treedef_tuple((tree_structure(consts), in_tree))
    assert self.vmap_rule is not None
    out_flat = custom_vmap_p.bind(*consts, *args_flat,
                                  call=closed_call,
                                  rule=ClosedRule(self.vmap_rule),
                                  in_tree=in_tree,
                                  out_tree=out_tree())
    return tree_unflatten(out_tree(), out_flat)
