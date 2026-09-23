def value_is_tensor_type(v):
    return value_has_tensors(v) and v['dynamic_type'] not in ['at::TensorList', 'const c10::List<c10::optional<at::Tensor>> &']
