def get_ema_multi_avg_fn(decay=0.999):
    """Get the function applying exponential moving average (EMA) across multiple params."""

    if decay < 0.0 or decay > 1.0:
        raise ValueError(
            f"Invalid decay value {decay} provided. Please provide a value in [0,1] range."
        )

    @torch.no_grad()
    def ema_update(ema_param_list: PARAM_LIST, current_param_list: PARAM_LIST, _):
        # foreach lerp only handles float and complex
        if torch.is_floating_point(ema_param_list[0]) or torch.is_complex(
            ema_param_list[0]
        ):
            torch._foreach_lerp_(ema_param_list, current_param_list, 1 - decay)
        else:
            for p_ema, p_model in zip(ema_param_list, current_param_list):
                p_ema.copy_(p_ema * decay + p_model * (1 - decay))

    return ema_update
