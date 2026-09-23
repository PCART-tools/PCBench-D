def serialize_arg_dict_as_script_module(arg_dict):
    arg_dict_flat = {arg_name: arg_value
                     for arg_name, arg_value in
                     arg_dict['input'] + arg_dict['target'] + arg_dict['extra_args'] + arg_dict['other']}
    arg_dict_module = torch.nn.Module()
    for arg_name, arg_value in arg_dict_flat.items():
        assert isinstance(arg_value, torch.Tensor)
        arg_dict_module.register_buffer(arg_name, arg_value)

    return torch.jit.script(arg_dict_module)
