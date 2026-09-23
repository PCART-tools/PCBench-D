def module_error_inputs_torch_nn_RNN_GRU(module_info, device, dtype, requires_grad, training, **kwargs):
    samples = [
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(10, 0, 1)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="hidden_size must be greater than zero"
        ),
        ErrorModuleInput(
            ModuleInput(constructor_input=FunctionInput(10, 10, 0)),
            error_on=ModuleErrorEnum.CONSTRUCTION_ERROR,
            error_type=ValueError,
            error_regex="num_layers must be greater than zero"
        ),
    ]
    return samples
