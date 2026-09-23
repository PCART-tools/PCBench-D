def reduce_window(operand, init_value, computation: Callable,
                  window_dimensions: core.Shape, window_strides: Sequence[int],
                  padding: Union[str, Sequence[Tuple[int, int]]],
                  base_dilation: Optional[Sequence[int]] = None,
                  window_dilation: Optional[Sequence[int]] = None) -> Array:
  """Wraps XLA's `ReduceWindowWithGeneralPadding
  <https://www.tensorflow.org/xla/operation_semantics#reducewindow>`_
  operator.
  """
  flat_operands, operand_tree = tree_util.tree_flatten(operand)
  flat_init_values, init_value_tree = tree_util.tree_flatten(init_value)
  if operand_tree != init_value_tree:
    raise ValueError('Operands must have the same tree structure as '
                     f'init_values: {operand_tree} vs. {init_value_tree}')
  if len(flat_operands) == 0:
    raise ValueError('reduce_window must have at least one operand.')
  if len(flat_operands) != len(flat_init_values):
    raise ValueError('Must have same total number of operands as init_values: '
                     f' {len(flat_operands)} vs. {len(flat_init_values)}')
  if isinstance(padding, str):
    dilated_window_dims = (
        window_dimensions if window_dilation is None else
        lax._dilate_shape(window_dimensions, window_dilation))
    padding = tuple(lax.padtype_to_pads(
        flat_operands[0].shape, dilated_window_dims, window_strides, padding))
  else:
    padding = tuple(padding)
  if base_dilation is None:
    base_dilation = (1,) * len(window_dimensions)
  if window_dilation is None:
    window_dilation = (1,) * len(window_dimensions)
  monoid_reducer = _get_monoid_window_reducer(computation, flat_init_values)
  if monoid_reducer:
    return monoid_reducer(operand, window_dimensions, window_strides, padding,
                          base_dilation, window_dilation)
  else:
    flat_init_avals = map(lax._abstractify, flat_init_values)
    jaxpr, consts, out_tree = lax._variadic_reduction_jaxpr(
        computation, tuple(flat_init_avals), init_value_tree)
    if operand_tree != out_tree:
      raise ValueError(
        'reduce_window output must have the same tree structure as the operands'
        f' {operand_tree} vs. {out_tree}')
    out_flat = reduce_window_p.bind(
        *flat_operands, *flat_init_values, jaxpr=jaxpr, consts=consts,
        window_dimensions=tuple(window_dimensions),
        window_strides=tuple(window_strides), padding=padding,
        base_dilation=tuple(base_dilation),
        window_dilation=tuple(window_dilation))
    return tree_util.tree_unflatten(out_tree, out_flat)
