def _find_choose_qparams_node(node: torch.fx.Node) -> Optional[torch.fx.Node]:
    # BFS to look for choose qparams
    from collections import deque

    queue = deque(list(node.users.keys()))
    while len(queue):
        n = queue.popleft()
        if n.op == "output":
            continue
        if n.op == "call_function" and n.target in _CHOOSE_QPARAMS_OPS:
            return n
        for k in n.users.keys():
            queue.append(k)
    return None
