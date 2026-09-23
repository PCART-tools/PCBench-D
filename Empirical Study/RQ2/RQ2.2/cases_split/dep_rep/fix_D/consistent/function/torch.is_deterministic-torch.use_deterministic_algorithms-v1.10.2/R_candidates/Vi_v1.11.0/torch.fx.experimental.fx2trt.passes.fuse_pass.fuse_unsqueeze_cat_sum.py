def fuse_unsqueeze_cat_sum(gm: torch.fx.GraphModule):
    for node in gm.graph.nodes:
        if node.target != acc_ops.sum:
            continue
        prev_node = node.kwargs["input"]
        if prev_node.target != acc_ops.cat or prev_node.kwargs["dim"] != 0:
            continue
        cat_inputs = prev_node.kwargs["tensors"]
        valid_pass = True
        for i in cat_inputs:
            if i.target != acc_ops.unsqueeze or i.kwargs["dim"] != 0:
                valid_pass = False
                break

        if not valid_pass:
            continue
        input_val = [i.kwargs["input"] for i in cat_inputs]

        with gm.graph.inserting_before(node):
            left = input_val[0]
            for i in range(1, len(input_val)):
                right = input_val[i]
                fused_node = gm.graph.call_function(acc_ops.add, kwargs={"input": left, "other": right})
                left = fused_node
        node.replace_all_uses_with(fused_node)

    gm.graph.eliminate_dead_code()
    gm.graph.lint()
    gm.recompile()
    return gm
