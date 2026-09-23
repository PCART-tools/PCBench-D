def fuse_sparse_matmul_add(gm: torch.fx.GraphModule):
    """
    Replace acc_ops.matmul + acc_ops.add with acc_ops.linear
    TRT8.2 can take advantage of structured sparsity (2:4), but the graph needs contain a single FC layer.
    Later versions of TRT should work with matmul.

    Example before:
    def forward(self, x):
        a = self.a
        b = self.b
        addmm_mm = torch.fx.experimental.fx_acc.acc_ops.matmul(input = a, other = b);  a = b = None
        addmm_add = torch.fx.experimental.fx_acc.acc_ops.add(input = addmm_mm, other = x);  addmm_mm = x = None
        return addmm_add

    After:
    def forward(self, x):
        a = self.a
        b = self.b
        linear_1 = torch.fx.experimental.fx_acc.acc_ops.linear(input = a, weight = b, bias = x);  a = b = x = None
        return linear_1
    """
    counter = 0
    for node in gm.graph.nodes:
        if node.target != acc_ops.add:
            continue
        add_node = node
        bias = add_node.kwargs["other"]

        if bias.op != "get_attr":
            continue
        # test that bias tensor is one-dimensional, should correspond to shape (out_features)
        if get_attr(bias).dim() > 1:
            continue

        node = add_node.kwargs["input"]
        if node.target != acc_ops.matmul:
            continue
        matmul_node = node
        a = matmul_node.kwargs["input"]

        node = matmul_node.kwargs["other"]
        if node.op != "get_attr":
            continue

        get_attr_node = node
        weight = get_attr(get_attr_node)
        # TODO: verify that weight comply with TRT structured sparsity requirements:
        # For each output channel and for each spatial pixel in the kernel weights,
        # every 4 input channels must have at least 2 zeros.

        # test that weight tensor is two-dimensional, should correspond to shape (out_features, in_features)
        if weight.dim() != 2:
            continue

        weight_t = weight.transpose(0, 1)
        weight_t_name = "weight_t_tensor_" + str(counter)
        gm.register_buffer(weight_t_name, weight_t)
        counter += 1

        with gm.graph.inserting_before(add_node):
            weight_t_attr = gm.graph.get_attr(weight_t_name)
            fused_node = gm.graph.call_function(acc_ops.linear, kwargs={"input": a, "weight": weight_t_attr, "bias": bias})
        add_node.replace_all_uses_with(fused_node)

    gm.graph.eliminate_dead_code()
    gm.graph.lint()
    gm.recompile()
    return gm
