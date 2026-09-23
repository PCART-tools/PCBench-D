def get_nightly_tests():

    configs = gen_build_env_list(False)
    filtered_configs = filter(predicate_exclude_macos, configs)

    tests = []
    for conf_options in filtered_configs:
        yaml_item = conf_options.gen_workflow_job("test", nightly=True)
        tests.append(yaml_item)

    return tests
