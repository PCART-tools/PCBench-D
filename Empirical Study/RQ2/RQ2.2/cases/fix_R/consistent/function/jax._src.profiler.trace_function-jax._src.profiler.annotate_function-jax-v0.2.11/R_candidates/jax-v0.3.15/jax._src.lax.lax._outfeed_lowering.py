def _outfeed_lowering(ctx, token, *xs, partitions):
  token_aval = ctx.avals_in[0]
  outfeed = mhlo.OutfeedOp(
      mlir.aval_to_ir_type(token_aval),
      mlir.flatten_lowering_ir_args(xs),
      token,
      outfeed_config=ir.StringAttr.get(''))
  if partitions is not None:
    mlir.set_sharding(outfeed, xla.sharding_to_proto(partitions))
  return outfeed.results
