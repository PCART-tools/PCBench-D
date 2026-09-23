def net2list(net_root):
    """
    Use topological order(BFS) to print the op of a net in a list
    """
    bfs_queue = []
    op_list = []
    cur = net_root
    for _, n in cur.ops.iteritems():
        bfs_queue.append(n)
    while bfs_queue:
        node = bfs_queue[0]
        bfs_queue = bfs_queue[1:]
        op_list.append(node.op)
        for _, n in node.ops.iteritems():
            bfs_queue.append(n)

    return op_list
