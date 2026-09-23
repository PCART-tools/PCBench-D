def _emit_tpu_python_callback(
    backend: xb.XlaBackend,
    ctx: LoweringRuleContext,
    callback,
    token: Optional[Any],
    operands: List[ir.Value],
    operand_avals: List[core.ShapedArray],
    operand_shapes: List[xc.Shape],
    result_avals: List[core.ShapedArray],
    result_shapes: List[xc.Shape],
    *,
    sharding: Optional[xc.OpSharding] = None
) -> Tuple[List[ir.Value], Any, Any]:
  token = token or hlo.CreateTokenOp().result
  _wrapped_callback = callback

  send_channels = []
  if not operand_avals:
    # If there are no operands to the callback, we need to insert a dummy send
    # op or the callback will never be triggered!
    # TODO(sharadmv,chky): Enable this fix in the runtime as opposed to in
    # MLIR builder.
    callback_without_args = _wrapped_callback
    def _wrapped_callback(*args):  # pylint: disable=function-redefined
      del args
      return callback_without_args()
    send_channel = ctx.module_context.new_channel()
    dummy_send_aval = core.ShapedArray((1,), np.float32)
    dummy_send_val = ir_constant(np.zeros(1, np.float32))
    operand_shapes = [*operand_shapes,
                      xla.aval_to_xla_shapes(dummy_send_aval)[0]]
    token = send_to_host(send_channel, token, dummy_send_val, dummy_send_aval,
                         callback.__name__, sharding=sharding)
    send_channels.append(send_channel)
  else:
    for operand, operand_aval in zip(operands, operand_avals):
      if any(s == 0 for s in operand_aval.shape):
        raise NotImplementedError(
            "Callbacks with zero-dimensional values not supported on TPU.")
      channel = ctx.module_context.new_channel()
      token = send_to_host(channel, token, operand, operand_aval,
                           callback.__name__, sharding=sharding)
      send_channels.append(channel)

  recv_channels = []
  outputs = []
  for result_aval in result_avals:
    if any(s == 0 for s in result_aval.shape):
      raise NotImplementedError(
          "Callbacks with zero-dimensional values not supported on TPU.")
    channel = ctx.module_context.new_channel()
    assert isinstance(result_aval, core.ShapedArray)
    token, out = receive_from_host(channel, token, result_aval,
                                   callback.__name__, sharding=sharding)
    outputs.append(out)
    recv_channels.append(channel)
  opaque = backend.make_python_callback_from_host_send_and_recv(
      _wrapped_callback, operand_shapes, result_shapes, send_channels,
      recv_channels)
  ctx.module_context.add_host_callback(opaque)
  return outputs, token, opaque
