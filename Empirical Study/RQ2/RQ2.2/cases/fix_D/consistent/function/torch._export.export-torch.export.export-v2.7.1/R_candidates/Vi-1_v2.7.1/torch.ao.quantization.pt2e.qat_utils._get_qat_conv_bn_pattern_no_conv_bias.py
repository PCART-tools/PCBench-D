def _get_qat_conv_bn_pattern_no_conv_bias(conv_fn: Callable) -> Callable:
    def _qat_conv_bn_pattern_no_conv_bias(
        x: torch.Tensor,
        conv_weight: torch.Tensor,
        # Not used, only for matching convenience
        conv_bias: torch.Tensor,
        bn_weight: torch.Tensor,
        bn_bias: torch.Tensor,
        bn_running_mean: torch.Tensor,
        bn_running_var: torch.Tensor,
    ) -> torch.Tensor:
        """
        Same as `_get_qat_conv_bn_pattern`, but handles the case with no conv bias.
        """
        # TODO: allow setting eps
        bn_eps = 1e-5
        running_std = torch.sqrt(bn_running_var + bn_eps)
        scale_factor = bn_weight / running_std
        weight_shape = [1] * len(conv_weight.shape)
        weight_in_channel_axis = 1 if _is_conv_transpose_fn(conv_fn) else 0
        weight_shape[weight_in_channel_axis] = -1
        bias_shape = [1] * len(conv_weight.shape)
        bias_shape[1] = -1
        scaled_weight = conv_weight * scale_factor.reshape(weight_shape)
        x = conv_fn(x, scaled_weight, None)
        x = x / scale_factor.reshape(bias_shape)
        x = F.batch_norm(
            x,
            bn_running_mean,
            bn_running_var,
            bn_weight,
            bn_bias,
            training=True,
            eps=bn_eps,
        )
        return x

    return _WrapperModule(_qat_conv_bn_pattern_no_conv_bias)
