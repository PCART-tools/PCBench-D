def module_inputs_torch_nn_AdaptiveAvgPool2d(module_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(3,),
                    forward_input=FunctionInput(make_input(shape=(1, 3, 5, 6))),
                    desc='single')]
