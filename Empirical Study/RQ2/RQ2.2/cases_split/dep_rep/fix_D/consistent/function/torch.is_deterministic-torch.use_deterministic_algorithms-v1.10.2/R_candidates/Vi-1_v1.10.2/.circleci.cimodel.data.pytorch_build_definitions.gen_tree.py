def gen_tree():
    root = get_root()
    configs_list = conf_tree.dfs(root)
    return configs_list
