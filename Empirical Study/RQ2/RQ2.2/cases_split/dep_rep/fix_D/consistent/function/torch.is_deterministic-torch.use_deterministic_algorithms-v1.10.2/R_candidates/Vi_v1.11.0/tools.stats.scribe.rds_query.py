def rds_query(queries: Union[Query, List[Query]]) -> Any:
    """
    Execute a simple read query on RDS. Queries should be of the form below,
    where everything except 'table_name' and 'fields' is optional.

    {
        "table_name": "my_table",
        "fields": ["something", "something_else"],
        "where": [
            {
                "field": "something",
                "value": 10
            }
        ],
        "group_by": ["something"],
        "order_by": ["something"],
        "limit": 5,
    }
    """
    if not isinstance(queries, list):
        queries = [queries]

    events = []
    for query in queries:
        events.append({"read": {**query}})

    return invoke_rds(events)
