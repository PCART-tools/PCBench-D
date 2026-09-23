def stage_backward_weight(
    weights: Iterator[Parameter], param_groups: list[dict[str, Any]], retain_graph=False
) -> tuple[Optional[torch.Tensor], ...]:
    # map weights to param_group_weights
    grad_acc_to_weight = {}
    weight_grads: list[Optional[torch.Tensor]] = []
    for index, weight in enumerate(weights):
        grad_acc = _get_grad_fn_or_grad_acc(weight)
        grad_acc_to_weight[grad_acc] = weight, index
        weight_grads.append(weight.grad)

    for param_group in param_groups:
        # TODO: Handle case where intermediate can have multiple outputs
        intermediate_edges = tuple(
            GradientEdge(i, 0) for i in param_group["intermediates"]
        )
        weights_edges = tuple(GradientEdge(w, 0) for w in param_group["params"])

        # Break a reference cycle caused inside stage_backward_input->get_hook->hook
        # The summarized cycle is:
        # `hook` -> cell -> param_group -> intermediates -> `hook`
        # becuase we install the hook function onto each of the intermediate autograd nodes.
        # We need to keep intermediates alive up until backward_weight, but we can free it now.
        del param_group["intermediates"]

        assert all(len(g) == 1 for g in param_group["grads"])
        # [NEW!] Able to pass a GradientEdge to autograd.grad as output
        # We do not need to retain_graph because... guarantee no overlap?
        # print("trying to execute: ", intermediate_edges, weights_edges)
        dweights = torch.autograd.grad(
            intermediate_edges,
            weights_edges,
            grad_outputs=sum(param_group["grads"], tuple()),
            retain_graph=retain_graph,
        )
        # release grad memory early after use
        del param_group["grads"]

        for grad_acc, dw in zip(param_group["params"], dweights):
            weight, index = grad_acc_to_weight[grad_acc]
            if weight.grad is None:
                weight.grad = dw
            else:
                weight.grad += dw
    # return grads in the original order weights were provided in
    return tuple(weight_grads)
