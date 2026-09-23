def register_rds_schema(table_name: str, schema: Dict[str, str]) -> None:
    """
    Register a table in RDS so it can be written to later on with 'rds_write'.
    'schema' should be a mapping of field names -> types, where supported types
    are 'int' and 'string'.

    Metadata fields such as pr, ref, branch, workflow_id, and build_environment
    will be added automatically.
    """
    base = {
        "pr": "string",
        "ref": "string",
        "branch": "string",
        "workflow_id": "string",
        "build_environment": "string",
    }

    event = [{"create_table": {"table_name": table_name, "fields": {**schema, **base}}}]

    invoke_rds(event)
