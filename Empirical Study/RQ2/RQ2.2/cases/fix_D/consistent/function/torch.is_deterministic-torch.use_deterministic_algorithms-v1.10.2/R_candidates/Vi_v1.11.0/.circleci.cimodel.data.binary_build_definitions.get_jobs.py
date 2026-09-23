def get_jobs(toplevel_key, smoke):
    jobs_list = []
    configs = gen_build_env_list(smoke)
    phase = "build" if toplevel_key == "binarybuilds" else "test"
    for build_config in configs:
        # don't test for macos_arm64 as it's cross compiled
        if phase != "test" or build_config.os != "macos_arm64":
            jobs_list.append(build_config.gen_workflow_job(phase, nightly=True))

    return jobs_list
