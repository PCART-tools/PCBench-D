def _append_qdq(x, is_per_channel, is_bias, kwargs):
    """
    Helper function to append q-dq ops after `x`, using dummy values for the qparams
    and qmin/qmax. We use dummy values here because we match with `ignore_literals=True`
    and will manually replace these values after subgraph rewriting.

    Return the dq node.
    """
    # Dummy args to be passed into q-dq ops
    per_channel_axis = 0
    scale_key = "bias_scale" if is_bias else "weight_scale"
    zp_key = "bias_zero_point" if is_bias else "weight_zero_point"
    scale = kwargs[scale_key] if is_per_channel else 1.0
    zp = kwargs[zp_key] if is_per_channel else 0
    qmin = -127
    qmax = 127
    dtype = torch.int8

    qd = torch.ops.quantized_decomposed
    if is_per_channel:
        x = qd.quantize_per_channel(x, scale, zp, per_channel_axis, qmin, qmax, dtype)
        x = qd.dequantize_per_channel(x, scale, zp, per_channel_axis, qmin, qmax, dtype)
    else:
        x = qd.quantize_per_tensor(x, scale, zp, qmin, qmax, dtype)
        x = qd.dequantize_per_tensor(x, scale, zp, qmin, qmax, dtype)
    return x
