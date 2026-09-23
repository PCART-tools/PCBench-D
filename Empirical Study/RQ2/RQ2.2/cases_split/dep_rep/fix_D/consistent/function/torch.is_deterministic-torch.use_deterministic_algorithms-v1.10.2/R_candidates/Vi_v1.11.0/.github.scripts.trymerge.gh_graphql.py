def gh_graphql(query: str, **kwargs: Any) -> Dict[str, Any]:
    rc = _fetch_url("https://api.github.com/graphql", data={"query": query, "variables": kwargs}, reader=json.load)
    if "errors" in rc:
        raise RuntimeError(f"GraphQL query {query} failed: {rc['errors']}")
    return cast(Dict[str, Any], rc)
