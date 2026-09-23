def _get_conv_bn_pattern(conv_fn: Callable) -> Callable:
    def _conv_bn_pattern(
        x: torch.Tensor,
        conv_weight: torch.Tensor,
        conv_bias: torch.Tensor,
        bn_weight: torch.Tensor,
        bn_bias: torch.Tensor,
        bn_running_mean: torch.Tensor,
        bn_running_var: torch.Tensor,
    ) -> torch.Tensor:
        x = conv_fn(x, conv_weight, conv_bias)
        x = F.batch_norm(
            x, bn_running_mean, bn_running_var, bn_weight, bn_bias, training=True
        )
        return x

    return _WrapperModule(_conv_bn_pattern)
