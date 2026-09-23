def invoke_rds(events: List[Dict[str, Any]]) -> Any:
    if not IS_GHA:
        sprint(f"Not invoking RDS lambda outside GitHub Actions:\n{events}")
        return

    return invoke_lambda("rds-proxy", events)
