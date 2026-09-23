def receive_from_host(channel: int, token: hlo.TokenType,
                      out_aval: core.ShapedArray, name: str, *,
                      sharding: xc.OpSharding | None = None) -> ir.Value:
  channel_handle = hlo.ChannelHandle.get(channel, RECV_FROM_HOST_TYPE)
  recv_op = hlo.RecvOp([aval_to_ir_type(out_aval),
                        hlo.TokenType.get()], token, channel_handle,
                        is_host_transfer=ir.BoolAttr.get(True))
  dtype_str = _dtype_to_xla_type_string(out_aval.dtype)
  if dtype_str in {"f64", "s64", "u64", "c64", "c128"}:
    raise NotImplementedError("64-bit types not supported.")
  recv_op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(
      dict(
          _xla_host_transfer_handler_name=ir.StringAttr.get(str(name)),
          _xla_host_transfer_original_type=ir.StringAttr.get(dtype_str),
          _xla_host_transfer_rendezvous=ir.StringAttr.get(str(name))))
  if sharding is not None:
    set_sharding(recv_op, sharding)
  # Token should be at the end of the results
  result, token = recv_op.results
  return token, result
