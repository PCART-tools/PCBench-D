def send_to_host(channel: int, token: hlo.TokenType, operand: Any,
                 aval: core.ShapedArray, name: str, *,
                 sharding: xc.OpSharding | None = None) -> ir.Value:
  channel_handle = hlo.ChannelHandle.get(channel, SEND_TO_HOST_TYPE)
  send_op = hlo.SendOp([operand], token, channel_handle,
                        is_host_transfer=ir.BoolAttr.get(True))
  dtype_str = _dtype_to_xla_type_string(aval.dtype)
  if dtype_str in {"f64", "s64", "u64", "c64", "c128"}:
    raise NotImplementedError("64-bit types not supported.")
  send_op.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(
      dict(
          _xla_host_transfer_handler_name=ir.StringAttr.get(str(name)),
          _xla_host_transfer_original_type=ir.StringAttr.get(dtype_str),
          _xla_host_transfer_rendezvous=ir.StringAttr.get(str(name))))
  if sharding is not None:
    set_sharding(send_op, sharding)
  return send_op.result
