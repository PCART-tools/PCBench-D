def check_dependency(partition):
    """Given a partition,check if there is a circular dependency on
    this partition using bfs
    """
    visited: Set[Partition] = set([partition])
    queue: List[Partition] = [partition]
    while queue:
        p = queue.pop(0)
        for child in p.children:
            if child == partition:
                return True
            else:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)
    return False
