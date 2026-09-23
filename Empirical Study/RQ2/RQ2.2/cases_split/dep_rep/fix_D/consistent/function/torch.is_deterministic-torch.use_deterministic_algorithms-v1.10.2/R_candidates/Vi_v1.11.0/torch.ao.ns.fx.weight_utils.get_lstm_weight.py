def get_lstm_weight(mod: nn.Module) -> List[torch.Tensor]:
    res = []
    for idx, param_name in enumerate(mod._flat_weights_names):  # type: ignore[arg-type]
        if 'weight_ih_l' in param_name or 'weight_hh_l' in param_name:
            param_value = mod._flat_weights[idx].detach()  # type: ignore[index]
            res.append(param_value)
    return res
