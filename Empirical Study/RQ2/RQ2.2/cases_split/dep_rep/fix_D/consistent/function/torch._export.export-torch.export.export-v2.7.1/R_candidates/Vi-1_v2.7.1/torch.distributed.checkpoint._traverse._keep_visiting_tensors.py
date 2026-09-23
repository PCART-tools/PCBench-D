def _keep_visiting_tensors(value: STATE_DICT_ITEM) -> bool:
    return isinstance(value, torch.Tensor)
