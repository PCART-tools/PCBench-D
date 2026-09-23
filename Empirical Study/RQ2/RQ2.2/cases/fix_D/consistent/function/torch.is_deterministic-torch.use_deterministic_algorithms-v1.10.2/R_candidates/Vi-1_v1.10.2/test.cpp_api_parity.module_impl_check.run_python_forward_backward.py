def run_python_forward_backward(unit_test_class, test_params):
    device = test_params.device
    module = test_params.test_instance.constructor(*test_params.test_instance.constructor_args).to(device)

    inputs = set_python_tensors_requires_grad(move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['input']], device))
    inputs += move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['target']], device)
    inputs += move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['extra_args']], device)

    # Some modules (such as `RReLU`) create random tensors in their forward pass.
    # To make sure the random tensors created are the same in Python/C++, we need
    # to set the RNG seed manually.
    torch.manual_seed(0)

    # Forward pass
    python_output = module(*inputs)

    # NOTE: This is a workaround to allow any module to be traced.
    # We can do this because we are only interested in transferring
    # the Python module's parameters and buffers to the C++ module.
    module.forward = types.MethodType(lambda self, input: input, module)
    script_module = torch.jit.trace(module, torch.tensor(0))

    # Backward pass
    python_output.sum().backward()

    # Put all gradients into a dict, to be compared later
    python_grad_dict = {}
    for name, param in module.named_parameters():
        grad = param.grad
        if grad.is_sparse:
            python_grad_dict[name + "_grad_indices"] = grad.coalesce().indices()
            python_grad_dict[name + "_grad_values"] = grad.coalesce().values()
        else:
            python_grad_dict[name + "_grad"] = grad

    return script_module, python_output, python_grad_dict
