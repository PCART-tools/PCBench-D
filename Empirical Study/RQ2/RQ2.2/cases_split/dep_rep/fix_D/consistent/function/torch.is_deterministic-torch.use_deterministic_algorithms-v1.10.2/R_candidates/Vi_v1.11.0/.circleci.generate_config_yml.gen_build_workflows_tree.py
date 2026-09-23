def gen_build_workflows_tree():
    build_workflows_functions = [
        cimodel.data.simple.android_definitions.get_workflow_jobs,
        cimodel.data.simple.mobile_definitions.get_workflow_jobs,
        cimodel.data.simple.binary_smoketest.get_workflow_jobs,
        cimodel.data.simple.nightly_ios.get_workflow_jobs,
        cimodel.data.simple.nightly_android.get_workflow_jobs,
        cimodel.data.simple.anaconda_prune_defintions.get_workflow_jobs,
        binary_build_definitions.get_post_upload_jobs,
        binary_build_definitions.get_binary_smoke_test_jobs,
    ]
    build_jobs = [f() for f in build_workflows_functions]
    build_jobs.extend(
        cimodel.data.simple.docker_definitions.get_workflow_jobs(
            # sort for consistency
            sorted(generate_required_docker_images(build_jobs))
        )
    )
    master_build_jobs = filter_master_only_jobs(build_jobs)

    binary_build_functions = [
        binary_build_definitions.get_binary_build_jobs,
        binary_build_definitions.get_nightly_tests,
        binary_build_definitions.get_nightly_uploads,
    ]

    return {
        "workflows": {
            "binary_builds": {
                "when": r"<< pipeline.parameters.run_binary_tests >>",
                "jobs": [f() for f in binary_build_functions],
            },
            "build": {
                "when": r"<< pipeline.parameters.run_build >>",
                "jobs": build_jobs,
            },
            "master_build": {
                "when": r"<< pipeline.parameters.run_master_build >>",
                "jobs": master_build_jobs,
            },
        }
    }
