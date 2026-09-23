def get_num_inputs(o):
    args = 0
    for a in o['arguments']:
        if a['type'] in ['at::TensorList', 'const c10::List<c10::optional<at::Tensor>> &']:
            return '*'
        elif value_has_tensors(a):
            args += 1
    return str(args)
