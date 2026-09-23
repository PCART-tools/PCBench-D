def rds_saved_query(query_names: Union[str, List[str]]) -> Any:
    """
    Execute a hardcoded RDS query by name. See
    https://github.com/pytorch/test-infra/blob/main/aws/lambda/rds-proxy/lambda_function.py#L52
    for available queries or submit a PR there to add a new one.
    """
    if not isinstance(query_names, list):
        query_names = [query_names]

    events = []
    for name in query_names:
        events.append({"read": {"saved_query_name": name}})

    return invoke_rds(events)
