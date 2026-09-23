def add_job(
    workflows: Dict[str, Any],
    workflow_name: str,
    type: str,
    job: Dict[str, Any],
    past_jobs: Dict[str, Any],
) -> None:
    """
    Add job 'job' under 'type' and 'workflow_name' to 'workflow' in place. Also
    add any dependencies (they must already be in 'past_jobs')
    """
    if workflow_name not in workflows:
        workflows[workflow_name] = {"when": "always", "jobs": []}

    requires = job.get("requires", None)
    if requires is not None:
        for requirement in requires:
            dependency = past_jobs[requirement]
            add_job(workflows, dependency["workflow_name"], dependency["type"], dependency["job"], past_jobs)

    workflows[workflow_name]["jobs"].append({type: job})
