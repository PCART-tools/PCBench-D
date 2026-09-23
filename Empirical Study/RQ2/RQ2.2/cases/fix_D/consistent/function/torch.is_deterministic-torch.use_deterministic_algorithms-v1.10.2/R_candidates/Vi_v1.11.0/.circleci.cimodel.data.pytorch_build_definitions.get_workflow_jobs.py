def get_workflow_jobs(only_slow_gradcheck=False):

    config_list = instantiate_configs(only_slow_gradcheck)

    x = []
    for conf_options in config_list:

        phases = conf_options.restrict_phases or dimensions.PHASES

        for phase in phases:

            # TODO why does this not have a test?
            if Conf.is_test_phase(phase) and conf_options.cuda_version == "10":
                continue

            x.append(conf_options.gen_workflow_job(phase))

        # TODO convert to recursion
        for conf in conf_options.get_dependents():
            x.append(conf.gen_workflow_job("test"))

    return x
