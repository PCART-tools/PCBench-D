def get_root(smoke, name):

    return binary_build_data.TopLevelNode(
        name,
        binary_build_data.CONFIG_TREE_DATA,
        smoke,
    )
