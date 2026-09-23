def quantize_rnn_modules(module, dtype=torch.int8):
    warnings.warn("quantize_rnn_modules function has been deprecated. "
                  "Please use torch.ao.quantization.quantize_dynamic API instead.")
    reassign = {}
    for name, mod in module.named_modules():
        if mod is module:
            continue
        new_mod = quantize_rnn_modules(mod, dtype)
        if new_mod is not mod:
            reassign[name] = new_mod

    for name, mod in reassign.items():
        setattr(module, name, mod)
    if isinstance(module, torch.nn.LSTM):
        if dtype != torch.int8 and dtype != torch.float16:
            raise RuntimeError("Unsupported dtype: {}".format(dtype))
        return QuantizedLSTM(module, dtype)
    if isinstance(module, torch.nn.GRU):
        return QuantizedGRU(module)
    return module
