def run_forward(unit_test_class, test_params):
    device = test_params.device

    inputs = set_python_tensors_requires_grad(move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['input']], device))
    inputs += move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['target']], device)
    inputs += move_python_tensors_to_device(
        [arg_value for _, arg_value in test_params.arg_dict['extra_args']], device)

    # Some functionals (such as `F.rrelu`) create random tensors in their call path.
    # To make sure the random tensors created are the same in Python/C++, we need
    # to set the RNG seed manually.
    torch.manual_seed(0)
    python_output = test_params.test_instance.constructor()(*inputs)

    return python_output
