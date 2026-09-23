def get_filtered_circleci_config(
    workflows: Dict[str, Any], relevant_jobs: List[str]
) -> Dict[str, Any]:
    """
    Given an existing CircleCI config, remove every job that's not listed in
    'relevant_jobs'
    """
    new_workflows: Dict[str, Any] = {}
    past_jobs: Dict[str, Any] = {}
    for workflow_name, workflow in workflows.items():
        if workflow_name not in WORKFLOWS_TO_CHECK:
            # Don't care about this workflow, skip it entirely
            continue

        for job_dict in workflow["jobs"]:
            for type, job in job_dict.items():
                if "name" not in job:
                    # Job doesn't have a name so it can't be handled
                    print("Skipping", type)
                else:
                    if job["name"] in relevant_jobs:
                        # Found a job that was specified at the CLI, add it to
                        # the new result
                        add_job(new_workflows, workflow_name, type, job, past_jobs)

                    # Record the job in case it's needed as a dependency later
                    past_jobs[job["name"]] = {
                        "workflow_name": workflow_name,
                        "type": type,
                        "job": job,
                    }

    return new_workflows
