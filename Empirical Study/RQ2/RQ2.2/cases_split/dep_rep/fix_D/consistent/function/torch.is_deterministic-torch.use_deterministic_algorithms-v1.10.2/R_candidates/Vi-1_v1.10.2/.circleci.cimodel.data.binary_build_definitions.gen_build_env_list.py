def gen_build_env_list(smoke):

    root = get_root(smoke, "N/A")
    config_list = conf_tree.dfs(root)

    newlist = []
    for c in config_list:
        conf = Conf(
            c.find_prop("os_name"),
            c.find_prop("gpu"),
            c.find_prop("package_format"),
            [c.find_prop("pyver")],
            c.find_prop("smoke") and not (c.find_prop("os_name") == "macos_arm64"),  # don't test arm64
            c.find_prop("libtorch_variant"),
            c.find_prop("gcc_config_variant"),
            c.find_prop("libtorch_config_variant"),
        )
        newlist.append(conf)

    return newlist
