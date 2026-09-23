def _compute_tree_height(g, root):
    ''' Compute the heights of the tree for all nodes
        Height of leaves are 0
    '''
    def _get_height(root):
        children = list(g.successors(root))
        height = 0
        if children:
            child_heights = [_get_height(x) for x in children]
            height = max(child_heights) + 1
        g.nodes[root]["height"] = height
        return height

    _get_height(root)
