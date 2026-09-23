def _resolve_delta_lake_uri(table_uri: str) -> tuple[str, str, str]:
    from urllib.parse import ParseResult, urlparse

    parsed_result = urlparse(table_uri)
    scheme = parsed_result.scheme

    resolved_uri = str(
        Path(table_uri).expanduser().resolve(True) if scheme == "" else table_uri
    )

    normalized_path = str(ParseResult("", *parsed_result[1:]).geturl())
    return (scheme, resolved_uri, normalized_path)
