class QueryParams(typing.Mapping[str, str]):
    """
    URL query parameters, as a multi-dict.
    """

    def __init__(self, *args: QueryParamTypes, **kwargs: typing.Any) -> None:
        assert len(args) < 2, "Too many arguments."
        assert not (args and kwargs), "Cannot mix named and unnamed arguments."

        value = args[0] if args else kwargs

        items: typing.Sequence[typing.Tuple[str, PrimitiveData]]
        if value is None or isinstance(value, (str, bytes)):
            value = value.decode("ascii") if isinstance(value, bytes) else value
            items = parse_qsl(value)
        elif isinstance(value, QueryParams):
            items = value.multi_items()
        elif isinstance(value, list):
            items = value
        else:
            items = flatten_queryparams(value)

        self._list = [(str(k), str_query_param(v)) for k, v in items]
        self._dict = {str(k): str_query_param(v) for k, v in items}

    def keys(self) -> typing.KeysView:
        return self._dict.keys()

    def values(self) -> typing.ValuesView:
        return self._dict.values()

    def items(self) -> typing.ItemsView:
        """
        Return all items in the query params. If a key occurs more than once
        only the first item for that key is returned.
        """
        return self._dict.items()

    def multi_items(self) -> typing.List[typing.Tuple[str, str]]:
        """
        Return all items in the query params. Allow duplicate keys to occur.
        """
        return list(self._list)

    def get(self, key: typing.Any, default: typing.Any = None) -> typing.Any:
        """
        Get a value from the query param for a given key. If the key occurs
        more than once, then only the first value is returned.
        """
        if key in self._dict:
            return self._dict[key]
        return default

    def get_list(self, key: typing.Any) -> typing.List[str]:
        """
        Get all values from the query param for a given key.
        """
        return [item_value for item_key, item_value in self._list if item_key == key]

    def update(self, params: QueryParamTypes = None) -> None:
        if not params:
            return

        params = QueryParams(params)
        for param in params:
            item, *extras = params.get_list(param)
            self[param] = item
            if extras:
                self._list.extend((param, e) for e in extras)
                # ensure getter matches merged QueryParams getter
                self._dict[param] = params[param]

    def __getitem__(self, key: typing.Any) -> str:
        return self._dict[key]

    def __setitem__(self, key: str, value: str) -> None:
        self._dict[key] = value

        found_indexes = []
        for idx, (item_key, _) in enumerate(self._list):
            if item_key == key:
                found_indexes.append(idx)

        for idx in reversed(found_indexes[1:]):
            del self._list[idx]

        if found_indexes:
            idx = found_indexes[0]
            self._list[idx] = (key, value)
        else:
            self._list.append((key, value))

    def __contains__(self, key: typing.Any) -> bool:
        return key in self._dict

    def __iter__(self) -> typing.Iterator[typing.Any]:
        return iter(self.keys())

    def __len__(self) -> int:
        return len(self._dict)

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return sorted(self._list) == sorted(other._list)

    def __str__(self) -> str:
        return urlencode(self._list)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        query_string = str(self)
        return f"{class_name}({query_string!r})"
