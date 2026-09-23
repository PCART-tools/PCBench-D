def verify_graph_equality(net_a, net_b):
    """
    Determines if the execution of two graphs are identical.
    That is, all inputs blobs are mapped to the same output blobs
    for each operator in their respective positions.

    This is meant to check the output of memonger with the original graph.
    It assumes that the nets have same external input and output.

    O(E) runtime + O(1) amortized cost to hash for python dict
    """

    def parent_list(ops):
        parent_list = [[] for _ in ops]
        edge_owner = {}
        for i, op in enumerate(ops):
            for blob in op.input:
                parent_id = edge_owner.get(blob)
                if parent_id is not None:
                    parent_list[i].append(parent_id)
            for blob in op.output:
                edge_owner[blob] = i

        return parent_list

    # Operator wise equality checks
    if (len(net_a.op) != len(net_b.op)):
        return False
    for op_a, op_b in zip(net_a.op, net_b.op):
        if (op_a.type != op_b.type or
                op_a.device_option != op_b.device_option or
                op_a.engine != op_b.engine):
            return False

    # Print debug info
    parent_list_a = parent_list(net_a.op)
    parent_list_b = parent_list(net_b.op)
    if parent_list_a != parent_list_b:
        j = 0
        for a, b in zip(parent_list_a, parent_list_b):
            if a != b:
                print("Difference {} vs {} \n {}".format(
                    j, net_a.op[j], net_b.op[j]))
                print("Parents: {} vs {}".format(a, b))

            j += 1

    # Net wise equality check
    return parent_list_a == parent_list_b
