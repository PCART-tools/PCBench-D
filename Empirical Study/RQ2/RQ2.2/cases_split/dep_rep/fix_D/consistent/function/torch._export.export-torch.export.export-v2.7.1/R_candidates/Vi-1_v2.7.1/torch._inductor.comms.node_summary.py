def node_summary(snode):
    detail = ""
    if isinstance(snode.node, ir.ExternKernelOut):
        detail = f" ({snode.node.python_kernel_name})"
    out_tensor_info = ""
    layout = snode.node.get_output_spec()
    if isinstance(layout, ir.Layout):
        out_tensor_info = f" (size={layout.size}, stride={layout.stride})"
    node_name = snode.node.maybe_get_name() or ""
    return f"{snode.node.__class__.__name__}{detail}{out_tensor_info} ({node_name})"
