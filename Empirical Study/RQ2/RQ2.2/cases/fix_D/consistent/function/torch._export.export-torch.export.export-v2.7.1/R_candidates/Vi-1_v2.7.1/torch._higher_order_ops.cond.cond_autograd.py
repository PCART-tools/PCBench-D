@cond_op.py_impl(DispatchKey.Autograd)
def cond_autograd(pred, true_fn, false_fn, operands):
    # A shortcut for the case where all inputs don't require gradient,
    # we skip tracing the forward and backward graph.
    if pytree.tree_all_only(
        torch.Tensor,
        lambda t: not t.requires_grad,  # type: ignore[union-attr]
        (pred, operands),
    ):
        with torch._C._AutoDispatchBelowAutograd():
            return cond_op(pred, true_fn, false_fn, operands)

    (
        fw_true_graph,
        fw_false_graph,
        joint_true_graph,
        joint_false_graph,
    ) = create_fw_bw_graph_branches(true_fn, false_fn, *operands)
    flat_out = CondAutogradOp.apply(
        pred,
        fw_true_graph,
        fw_false_graph,
        joint_true_graph,
        joint_false_graph,
        *operands,
    )
    return flat_out
