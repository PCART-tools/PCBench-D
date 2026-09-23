def _infeed_lowering(ctx, token, *, shapes, partitions):
  output_types = safe_map(mlir.aval_to_ir_types, ctx.avals_out[:-1])
  flat_output_types = util.flatten(output_types)
  # TODO(phawkins): verify `shapes` have a major-to-minor layout.
  layouts = ir.ArrayAttr.get([
      ir.ArrayAttr.get(
          [mlir.i64_attr(i)
           for i in range(len(aval.shape) - 1, -1, -1)])
      for aval in shapes
  ])
  infeed = mhlo.InfeedOp(
      flat_output_types + [mhlo.TokenType.get()],
      token,
      infeed_config=ir.StringAttr.get(''),
      layout=layouts)
  if partitions is not None:
    mlir.set_sharding(infeed, xla.sharding_to_proto(partitions))
  token = infeed.results[-1]
  outs = infeed.results[:-1]
  return util.unflatten(outs, safe_map(len, output_types)) + [[
      token,
  ]]
