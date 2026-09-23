def _get_grad(net, outputs, outputs_with_grad, input_values, inputs_with_grads):
    grad_net = net.Clone(net.Name() + "_copy")
    grad_map = grad_net.AddGradientOperators(outputs_with_grad)

    for name, value in (input_values or {}).items():
        workspace.blobs[name] = value

    for input_to_check in inputs_with_grads:
        assert input_to_check in grad_map, (
            '{} has no gradient, cannot check net gradient.'.format(
                input_to_check))
        assert str(input_to_check) in workspace.blobs

    workspace.RunNetOnce(grad_net)
    forward_results = [(output, workspace.blobs[output]) for output in outputs]
    grads = {input_to_check: _get_grad_blob(grad_map, input_to_check)
             for input_to_check in inputs_with_grads}

    return forward_results, grads, grad_net
