def optimize_interference(net, static_blobs,
                          ordering_function=topological_sort_traversal,
                          blob_sizes=None,
                          algo=AssignmentAlgorithm.GREEDY):
    """
    ordering_function: topological_sort_traversal or
                       topological_sort_traversal_longest_path.
                       topological_sort_traversal_longest_path gives better
                       results but needs a bit more computation.
    algo: Method used to find assignments (AssignmentAlgorithm.GREEDY or
          AssignmentAlgorithm.DYNAMIC_PROGRAMMING).
          AssignmentAlgorithm.DYNAMIC_PROGRAMMING gives optimal solution at the
          cost of more computation.
          AssignmentAlgorithm.GREEDY may be better in the case 'blob_sizes' is
          not provided.
    """

    """
    1) Use a BFS traversal of the execution graph to generate an
       ordering of the node executions.
    2) Generate use-def ranges for each `blob` in the BFS traversal
       order.
    3) Assign blobs to `canonical blobs`
    4) Rename blobs to canonical blobs
    """

    net = copy.deepcopy(net)
    g = compute_interference_graph(net.op)
    ordering = ordering_function(g)
    linearized_ops = [net.op[i] for i in ordering]

    # Reorder ops in net based on the computed linearlized order.
    # If the graph has multiple topological orderings and if the NetDef's
    # ordering differs from the order used to compute ranges, then the
    # runtime might end up overwriting blobs before they are used.
    del net.op[:]
    net.op.extend(linearized_ops)

    ranges = compute_ranges(linearized_ops, blob_sizes)
    assignments = compute_assignments(ranges, static_blobs, algo)
    blob_assignments = compute_blob_assignments(assignments)
    apply_assignments(net, blob_assignments)
    return Optimization(
        net=net,
        blob_assignments=blob_assignments,
        assignments=assignments)
