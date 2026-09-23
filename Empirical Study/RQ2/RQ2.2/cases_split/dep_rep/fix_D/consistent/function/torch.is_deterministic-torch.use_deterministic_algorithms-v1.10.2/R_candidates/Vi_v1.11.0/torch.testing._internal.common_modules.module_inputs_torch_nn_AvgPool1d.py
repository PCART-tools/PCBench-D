def module_inputs_torch_nn_AvgPool1d(module_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return [
        ModuleInput(constructor_input=FunctionInput(kernel_size=2),
                    forward_input=FunctionInput(make_input(shape=(3, 6))),
                    desc='no_batch_dim',
                    reference_fn=no_batch_dim_reference_fn)]
