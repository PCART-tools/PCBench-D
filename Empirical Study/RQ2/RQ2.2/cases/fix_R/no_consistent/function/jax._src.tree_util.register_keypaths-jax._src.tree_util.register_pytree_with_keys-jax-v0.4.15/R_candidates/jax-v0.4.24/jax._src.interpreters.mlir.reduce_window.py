def reduce_window(
    ctx: LoweringRuleContext,
    *,
    # Base name to be used for the reducer function
    reducer_name: str,
    # Compute the reducer body given the reducer.
    reducer_body: Callable[[ir.Block], Sequence[ir.Value]],
    operands: Sequence[ir.Value],
    init_values: Sequence[ir.Value],
    init_values_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue],
    window_dimensions, window_strides, padding, base_dilation, window_dilation):
  """Builds a ReduceWindowOp, with support for dynamic shapes."""

  scalar_types = [aval_to_ir_type(aval) for aval in init_values_avals]
  if any(not core.is_constant_shape(s)
         for s in [window_dimensions, window_dilation, window_strides, base_dilation, *padding]):
    # d_padding will be an array i32[N, 2] with pad_lo and pad_hi for each
    # spatial dimension.
    int2d = aval_to_ir_type(core.ShapedArray((1, 2), np.int32))
    def prep_one_pad(pad_lo_hi: tuple[core.DimSize, core.DimSize]):
      pads = eval_dynamic_shape_as_tensor(ctx, pad_lo_hi)  # i32[2]
      return hlo.reshape(int2d, pads)
    d_padding = hlo.concatenate(list(map(prep_one_pad, padding)), i64_attr(0))
    # Build the reducer
    reducer_type = ir.FunctionType.get(scalar_types + scalar_types,
                                       scalar_types)
    with ir.InsertionPoint.at_block_begin(ctx.module_context.module.body):
      reducer = func_dialect.FuncOp(reducer_name, reducer_type)
    ctx.module_context.symbol_table.insert(reducer)
    entry_block = reducer.add_entry_block()
    with ir.InsertionPoint(entry_block):
      hlo.return_(reducer_body(entry_block))

    rw = custom_call(
      "stablehlo.dynamic_reduce_window",
      result_types=list(map(aval_to_ir_type, out_avals)),
      operands=[
        *operands, *init_values,
        eval_dynamic_shape_as_tensor(ctx, window_dimensions),
        eval_dynamic_shape_as_tensor(ctx, window_strides),
        eval_dynamic_shape_as_tensor(ctx, base_dilation),
        eval_dynamic_shape_as_tensor(ctx, window_dilation),
        d_padding],
       called_computations=[reducer.name.value],
    )
  else:  # Static shapes
    rw = hlo.ReduceWindowOp(
        list(map(aval_to_ir_type, out_avals)),
        operands, init_values,
        dense_int_array_v6(window_dimensions),
        window_strides=dense_int_array_v6(window_strides),
        base_dilations=dense_int_array_v6(base_dilation),
        window_dilations=dense_int_array_v6(window_dilation),
        padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                            shape=(len(padding), 2)))
    reducer = rw.regions[0].blocks.append(*(scalar_types + scalar_types))
    with ir.InsertionPoint(reducer):
      hlo.return_(reducer_body(reducer))
  return rw.results
