def _resolve_delta_lake_uri(table_uri: str, *, strict: bool = True) -> str:
    parsed_result = urlparse(table_uri)

    resolved_uri = str(
        Path(table_uri).expanduser().resolve(strict)
        if parsed_result.scheme == ""
        else table_uri
    )

    return resolved_uri
