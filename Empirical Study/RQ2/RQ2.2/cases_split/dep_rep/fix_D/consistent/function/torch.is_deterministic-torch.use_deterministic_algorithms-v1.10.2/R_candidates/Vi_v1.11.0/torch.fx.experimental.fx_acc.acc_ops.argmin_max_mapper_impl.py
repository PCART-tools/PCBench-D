def argmin_max_mapper_impl(node: torch.fx.Node, largest: bool) -> torch.fx.Node:
    """
    Map torch.argmin or torch.argmax to acc_ops.flatten (depend on dim) + acc_ops.topk
    + acc_ops.getitem + acc_ops.squeeze (depends on keepdim).
    """
    input_node = node.kwargs["input"]
    dim = node.kwargs["dim"]
    keepdim = node.kwargs["keepdim"]

    if dim is None and keepdim:
        raise RuntimeError(
            "We currently don't support argmin/argmax with dim=None and keepdim=True"
        )

    with node.graph.inserting_before(node):
        if dim is None:
            flatten_kwargs = {
                "input": node.kwargs["input"],
                "start_dim": 0,
                "end_dim": -1,
            }
            flatten_node = node.graph.call_function(flatten, kwargs=flatten_kwargs)
            flatten_node.meta["type"] = torch.Tensor
            input_node = flatten_node
            dim = -1

        topk_kwargs = {
            "input": input_node,
            "k": 1,
            "dim": dim,
            "largest": largest,
            "sorted": False,
        }
        topk_node = node.graph.call_function(topk, kwargs=topk_kwargs)
        # It's actually more like NamedTuple but tuple here should be fine.
        topk_node.meta["type"] = tuple

        getitem_kwargs = {"input": topk_node, "idx": 1}
        getitem_node = node.graph.call_function(getitem, kwargs=getitem_kwargs)
        getitem_node.meta["type"] = torch.Tensor
        output_node = getitem_node

        if not keepdim:
            squeeze_kwargs = {"input": getitem_node, "dim": dim}
            output_node = node.graph.call_function(squeeze, kwargs=squeeze_kwargs)

        output_node.meta = node.meta.copy()
        return output_node
