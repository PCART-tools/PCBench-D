def _gen_subgradient_pass(subnet, init_grad):
    from caffe2.python.core import IR
    subnet_ir = IR(subnet.op)
    grad_ops, grad_blob_map = \
        subnet_ir.GetBackwardPass(init_grad)
    grad_names_map = {}
    for b, g in grad_blob_map.items():
        grad_names_map[str(b)] = str(g)
    return grad_ops, grad_names_map
