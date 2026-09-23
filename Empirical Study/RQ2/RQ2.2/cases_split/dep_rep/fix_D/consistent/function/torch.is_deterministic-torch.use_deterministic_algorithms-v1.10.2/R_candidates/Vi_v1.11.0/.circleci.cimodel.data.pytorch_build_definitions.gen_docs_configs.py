def gen_docs_configs(xenial_parent_config):
    configs = []

    configs.append(
        HiddenConf(
            "pytorch_python_doc_build",
            parent_build=xenial_parent_config,
            filters=gen_filter_dict(branches_list=["master", "nightly"],
                                    tags_list=RC_PATTERN),
        )
    )
    configs.append(
        DocPushConf(
            "pytorch_python_doc_push",
            parent_build="pytorch_python_doc_build",
            branch="site",
        )
    )

    configs.append(
        HiddenConf(
            "pytorch_cpp_doc_build",
            parent_build=xenial_parent_config,
            filters=gen_filter_dict(branches_list=["master", "nightly"],
                                    tags_list=RC_PATTERN),
        )
    )
    configs.append(
        DocPushConf(
            "pytorch_cpp_doc_push",
            parent_build="pytorch_cpp_doc_build",
            branch="master",
        )
    )
    return configs
