def fallback_node_due_to_unsupported_type(node: torch.fx.Node, allow_cpu_inputs=True):
    # Custom fallback lowering
    if node.target is aten.view_as_complex.default:
        return False

    # We should be able to remove this special case once `disable_cpp_codegen` is killed.
    if node.target is aten.lift_fresh_copy.default:
        return False

    def check_skip_condition(node, parent, is_output):
        if not isinstance(node, torch.fx.Node):
            return False

        if "val" not in node.meta:
            return False

        for meta in pytree.tree_leaves(node.meta["val"]):
            if not isinstance(meta, torch._subclasses.FakeTensor):
                continue

            if is_output:
                if unsupported_output_tensor(meta, parent, node):
                    return True
            else:
                if unsupported_input_tensor(meta, parent, node):
                    return True

        return False

    # only skip codegen if there is a cpu output, not input
    for arg in pytree.arg_tree_leaves(*node.args, **node.kwargs):
        if check_skip_condition(arg, node, is_output=False):
            return True

    return check_skip_condition(node, node, is_output=True)
