@custom_api_util.register_custom_decorator_type
class custom_transpose:
  fun: Callable
  transpose: Optional[Callable] = None

  def __init__(self, fun: Callable):
    functools.update_wrapper(self, fun)
    self.fun = fun  # type: ignore[assignment]

  __getattr__ = custom_api_util.forward_attr

  def def_transpose(self, transpose: Callable):
    self.transpose = transpose
    return transpose

  @traceback_util.api_boundary
  def __call__(self, out_types, res_arg, lin_arg):
    _, res_tree = tree_flatten(res_arg)
    _, lin_tree = tree_flatten(lin_arg)
    args_flat, in_tree = tree_flatten((res_arg, lin_arg))

    # TODO(frostig,mattjj): check that out_trees match
    # TODO(frostig,mattjj): could, and should, we avoid flattening
    # self.fun at this point?

    flat_fun, out_tree2 = flatten_fun_nokwargs(lu.wrap_init(self.fun), in_tree)
    out_types_flat, out_tree = tree_flatten(out_types)
    out_flat = custom_transpose_p.bind(flat_fun, *args_flat,
                                       transpose=self.transpose,
                                       out_types=out_types_flat,
                                       lin_tree=lin_tree,
                                       res_tree=res_tree,
                                       out_tree=out_tree)
    return tree_unflatten(out_tree, out_flat)
