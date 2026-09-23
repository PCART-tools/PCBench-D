def clear_torch_function_mode_stack():
    for _ in range(_len_torch_function_stack()):
        _pop_torch_function_stack()
