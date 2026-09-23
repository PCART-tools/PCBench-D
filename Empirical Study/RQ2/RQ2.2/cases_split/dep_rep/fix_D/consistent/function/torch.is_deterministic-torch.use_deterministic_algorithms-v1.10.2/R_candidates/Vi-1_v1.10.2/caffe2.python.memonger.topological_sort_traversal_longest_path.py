def topological_sort_traversal_longest_path(g):
    ''' The graph 'g' may contain several source nodes (nodes without incoming
        edge), which could be in any order and still be a valid
        topological sorting result. We would like to arrange these source nodes
        so that the average live spans of the computed blobs are shorter.
        The idea is to sort the source nodes based on the length of their path to
        the target node so that the one with longer path is used first.
        This is done by:
        - Add a single target node if there are multiple target nodes in 'g'.
        - Find the longest path between each source and the target node.
        - Convert the longest paths to a tree with the target node being the root
          and source nodes being the leaves.
        - Sort the nodes of the tree based on the height of the tree.
    '''
    gt = _add_single_target_ifneeded(g)
    source_nodes = _find_source_nodes(gt)
    lpaths = _get_longest_paths(gt, source_nodes)
    tree, root = _build_tree(list(viewvalues(lpaths)))
    sorted_sources = _sort_tree_leaves(tree, root)
    assert(sorted(sorted_sources) == sorted(source_nodes))

    if nx.__version__ < '2.0':
        ret = nx.topological_sort(g, sorted_sources)
    else:
        # Manually making a sorted descendent list
        dependency_order = list(sorted_sources)
        seen_nodes = set(sorted_sources)
        for s in sorted_sources:
            desc = nx.descendants(g, s)
            for d in desc:
                if d not in seen_nodes:
                    seen_nodes.add(d)
                    dependency_order.append(d)
        sort_key = dict((v, len(dependency_order) - i) for i, v in enumerate(dependency_order))
        ret = nx.algorithms.dag.lexicographical_topological_sort(
            g, key=lambda x: sort_key[x])
        ret = list(ret)
    assert(len(ret) == len(g.nodes))
    return ret
