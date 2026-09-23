def dfs(toplevel_config_node):

    config_list = []

    def leaf_callback(node):
        config_list.append(node)

    dfs_recurse(toplevel_config_node, leaf_callback)

    return config_list
