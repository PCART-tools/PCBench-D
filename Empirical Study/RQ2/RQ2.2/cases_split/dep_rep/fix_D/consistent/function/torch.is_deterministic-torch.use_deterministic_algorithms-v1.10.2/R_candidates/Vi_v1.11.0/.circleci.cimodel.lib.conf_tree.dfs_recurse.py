def dfs_recurse(
        node,
        leaf_callback=lambda x: None,
        discovery_callback=lambda x, y, z: None,
        child_callback=lambda x, y: None,
        sibling_index=0,
        sibling_count=1):

    discovery_callback(node, sibling_index, sibling_count)

    node_children = node.get_children()
    if node_children:
        for i, child in enumerate(node_children):
            child_callback(node, child)

            dfs_recurse(
                child,
                leaf_callback,
                discovery_callback,
                child_callback,
                i,
                len(node_children),
            )
    else:
        leaf_callback(node)
