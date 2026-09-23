def _load_weight_qparams(
        self, state_dict, prefix, local_metadata, strict,
        missing_keys, unexpected_keys, error_msgs):
    key = prefix + "_weight_qparams"
    if key in state_dict:
        self._weight_qparams = state_dict[key]
        state_dict.pop(key)
