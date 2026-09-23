def _sort_tree_leaves(g, root):
    ''' For each node, sort its child nodes based on the height of the nodes.
        Return the leaf nodes of the tree after sorting.
    '''
    def _get_height(root):
        return g.nodes[root]["height"]

    def _get_sorted_leaves(root):
        children = list(g.successors(root))
        if not children:
            return [root]
        child_heights = [_get_height(x) for x in children]
        order = sorted(range(len(children)), key=lambda x: child_heights[x])
        ret = []
        for co in order:
            cr = children[co]
            ret += _get_sorted_leaves(cr)

        return ret

    return _get_sorted_leaves(root)
