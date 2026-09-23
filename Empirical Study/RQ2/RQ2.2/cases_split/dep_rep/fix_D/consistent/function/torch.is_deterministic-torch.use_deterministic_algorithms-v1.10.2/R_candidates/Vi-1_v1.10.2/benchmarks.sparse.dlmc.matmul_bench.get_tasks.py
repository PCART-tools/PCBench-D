def get_tasks(op, backward_test, device):
    def filter_ops(operation):
        if backward_test:
            test_name = device + ":matmul-backward"
            return [
                (test_name, device, "torch:" + operation.replace("sparse", "dense"),
                 "matmul_backward(dx, dy, grad_output)"),
                (test_name, device, "torch:" + operation, "sparse_matmul_backward(x, y, sparse_grad_output)")
            ]
        else:
            test_name = device + ":matmul-forward"
            return list(filter(None, [
                (test_name, device, "torch:" + operation.replace("sparse", "dense"),
                 "{}(dx, dy)".format(OPS_MAP[operation])),
                (test_name, device, "torch:" + operation, "{}(x, y)".format(OPS_MAP[operation])),
                (test_name, device, "scipy:" + operation, "scipy_matmul(sx, sy)") if device == "cpu" else None
            ]))

    all_operations = {
        "sparse@sparse": filter_ops("sparse@sparse"),
        "sparse@dense": filter_ops("sparse@dense"),
        "sparse@vector": filter_ops("sparse@vector"),
    }
    return all_operations[op]
