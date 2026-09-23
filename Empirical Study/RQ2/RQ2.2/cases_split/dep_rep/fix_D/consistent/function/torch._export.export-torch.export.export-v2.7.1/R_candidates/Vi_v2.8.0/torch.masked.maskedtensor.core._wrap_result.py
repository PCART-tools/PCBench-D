def _wrap_result(result_data, result_mask):
    if isinstance(result_data, list):
        return [_wrap_result(r, m) for (r, m) in zip(result_data, result_mask)]
    if isinstance(result_data, tuple):
        return tuple(_wrap_result(r, m) for (r, m) in zip(result_data, result_mask))
    if torch.is_tensor(result_data):
        return MaskedTensor(result_data, result_mask)
    # Expect result_data and result_mask to be Tensors only
    return NotImplemented
