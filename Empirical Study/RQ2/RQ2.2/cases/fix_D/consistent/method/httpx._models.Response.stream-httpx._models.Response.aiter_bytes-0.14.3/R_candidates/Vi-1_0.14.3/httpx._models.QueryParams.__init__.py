    def __init__(self, *args: QueryParamTypes, **kwargs: typing.Any) -> None:
        assert len(args) < 2, "Too many arguments."
        assert not (args and kwargs), "Cannot mix named and unnamed arguments."

        value = args[0] if args else kwargs

        items: typing.Sequence[typing.Tuple[str, PrimitiveData]]
        if value is None or isinstance(value, str):
            items = parse_qsl(value)
        elif isinstance(value, QueryParams):
            items = value.multi_items()
        elif isinstance(value, list):
            items = value
        else:
            items = flatten_queryparams(value)

        self._list = [(str(k), str_query_param(v)) for k, v in items]
        self._dict = {str(k): str_query_param(v) for k, v in items}
