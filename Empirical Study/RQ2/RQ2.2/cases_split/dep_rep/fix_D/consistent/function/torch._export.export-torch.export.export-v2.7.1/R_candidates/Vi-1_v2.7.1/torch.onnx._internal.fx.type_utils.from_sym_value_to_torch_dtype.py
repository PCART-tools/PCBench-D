def from_sym_value_to_torch_dtype(sym_value: SYM_VALUE_TYPE) -> torch.dtype:
    return _SYM_TYPE_TO_TORCH_DTYPE[type(sym_value)]
