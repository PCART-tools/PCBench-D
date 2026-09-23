def get_lstm_mod_weights(mod: nn.Module) -> List[torch.Tensor]:
    # TODO(future PR): make more generic, handle everything
    if isinstance(mod, nn.LSTM):
        res = []
        for idx, param_name in enumerate(mod._flat_weights_names):
            if 'weight_ih_l' in param_name or 'weight_hh_l' in param_name:
                param_value = mod._flat_weights[idx].detach()
                res.append(param_value)
        return res
    else:
        assert isinstance(mod, nnqd.LSTM), f"type {type(res)} not handled yet"
        res = []
        for weight_value in mod._all_weight_values:
            res.append(weight_value.param.__getstate__()[0][4][0].__getstate__()[0][0])
            res.append(weight_value.param.__getstate__()[0][4][1].__getstate__()[0][0])
        return res
