def _approx_top_k_jvp(primals, tangents, *, k, reduction_dimension,
                      recall_target, is_max_k, reduction_input_size_override,
                      aggregate_to_topk):
  operand, = primals
  tangent, = tangents
  if is_max_k:
    val_out, arg_out = approx_max_k(operand, k, reduction_dimension,
                                    recall_target,
                                    reduction_input_size_override,
                                    aggregate_to_topk)
  else:
    val_out, arg_out = approx_min_k(operand, k, reduction_dimension,
                                    recall_target,
                                    reduction_input_size_override,
                                    aggregate_to_topk)
  if type(tangent) is ad_util.Zero:
    tangent_out = ad_util.Zero.from_value(val_out)
  else:
    arg_shape = arg_out.shape
    rank = len(arg_shape)
    if reduction_dimension < 0:
      reduction_dimension += rank
    iotas = [
        lax.broadcasted_iota(arg_out.dtype, arg_shape, i) for i in range(rank)
    ]
    idx = tuple(
        arg_out if i == reduction_dimension else iotas[i] for i in range(rank))
    tangent_out = tangent[idx]
  return (val_out, arg_out), (tangent_out, ad_util.Zero.from_value(arg_out))
