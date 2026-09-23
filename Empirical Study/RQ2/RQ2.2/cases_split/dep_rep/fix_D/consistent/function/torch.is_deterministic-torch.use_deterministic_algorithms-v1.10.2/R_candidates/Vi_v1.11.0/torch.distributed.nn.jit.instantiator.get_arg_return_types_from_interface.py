def get_arg_return_types_from_interface(module_interface):
    assert getattr(
        module_interface, "__torch_script_interface__", False
    ), "Expect a TorchScript class interface decorated by @torch.jit.interface."
    qualified_name = torch._jit_internal._qualified_name(module_interface)
    cu = torch.jit._state._python_cu
    module_interface_c = cu.get_interface(qualified_name)
    assert (
        "forward" in module_interface_c.getMethodNames()
    ), "Expect forward in interface methods, while it has {}".format(
        module_interface_c.getMethodNames()
    )
    method_schema = module_interface_c.getMethod("forward")

    arg_str_list = []
    arg_type_str_list = []
    assert method_schema is not None
    for argument in method_schema.arguments:
        arg_str_list.append(argument.name)

        if argument.has_default_value():
            default_value_str = " = {}".format(argument.default_value)
        else:
            default_value_str = ""
        arg_type_str = "{name}: {type}{default_value}".format(
            name=argument.name, type=argument.type, default_value=default_value_str
        )
        arg_type_str_list.append(arg_type_str)

    arg_str_list = arg_str_list[1:]  # Remove "self".
    args_str = ", ".join(arg_str_list)

    arg_type_str_list = arg_type_str_list[1:]  # Remove "self".
    arg_types_str = ", ".join(arg_type_str_list)

    assert len(method_schema.returns) == 1
    argument = method_schema.returns[0]
    return_type_str = str(argument.type)

    return args_str, arg_types_str, return_type_str
