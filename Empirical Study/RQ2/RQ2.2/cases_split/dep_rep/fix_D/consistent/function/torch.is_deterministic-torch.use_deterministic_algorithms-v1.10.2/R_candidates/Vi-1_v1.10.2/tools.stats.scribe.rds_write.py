def rds_write(
    table_name: str,
    values_list: List[Dict[str, Any]],
    only_on_master: bool = True,
    only_on_jobs: Optional[List[str]] = None,
) -> None:
    """
    Note: Only works from GitHub Actions CI runners

    Write a set of entries to a particular RDS table. 'table_name' should be
    a table registered via 'register_rds_schema' prior to calling rds_write.
    'values_list' should be a list of dictionaries that map field names to
    values.
    """
    sprint("Writing for", os.getenv("CIRCLE_PR_NUMBER"))
    is_master = os.getenv("CIRCLE_PR_NUMBER", "").strip() == ""
    if only_on_master and not is_master:
        sprint("Skipping RDS write on PR")
        return

    pr = os.getenv("CIRCLE_PR_NUMBER", None)
    if pr is not None and pr.strip() == "":
        pr = None

    build_environment = os.environ.get("BUILD_ENVIRONMENT", "").split()[0]
    if only_on_jobs is not None and build_environment not in only_on_jobs:
        sprint(f"Skipping write since {build_environment} is not in {only_on_jobs}")
        return

    base = {
        "pr": pr,
        "ref": os.getenv("CIRCLE_SHA1"),
        "branch": os.getenv("CIRCLE_BRANCH"),
        "workflow_id": os.getenv("GITHUB_RUN_ID"),
        "build_environment": build_environment,
    }

    events = []
    for values in values_list:
        events.append(
            {"write": {"table_name": table_name, "values": {**values, **base}}}
        )

    sprint("Wrote stats for", table_name)
    invoke_rds(events)
